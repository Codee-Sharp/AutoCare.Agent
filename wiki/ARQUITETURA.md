# 🏗️ ARQUITETURA DO SISTEMA

## Visão Geral Técnica

O AutoCare Agent é construído como um **microserviço especializado em IA** que fica **atrás de uma aplicação interna existente**, com separação clara:

1. **Camada de Interação** (LLM + Orquestração)
2. **Camada de Integração** (REST API com aplicação interna)
3. **Camada de Cache** (Redis local)

A **Aplicação Interna** é responsável por:
- Receber requisições de múltiplas fontes
- Orquestrar chamadas ao Agent
- Gerenciar estado e persistência
- Processar pagamentos
- Distribuir notificações

---

## 0. Integração com Aplicação Interna

### 0.1 Posicionamento Arquitetural

O Agent NÃO funciona de forma isolada. Ele é um **microserviço consumidor** que:
- Recebe requests REST da aplicação interna
- Processa conversas via LLM
- Retorna respostas estruturadas
- Consulta APIs da aplicação interna para dados críticos

```
┌─────────────────────────────────────────┐
│  Aplicação Interna (Orquestradora)      │
│  ├─ REST endpoints                      │
│  ├─ Banco PostgreSQL                    │
│  ├─ Payment processor                   │
│  └─ Messaging queue                     │
└────────────┬────────────────────────────┘
             │ REST
             ▼
┌─────────────────────────────────────────┐
│  AutoCare Agent (LLM Processor)         │
│  ├─ Python + LangGraph                  │
│  ├─ LLM Client (Composer 2)             │
│  ├─ Tool Calling                        │
│  └─ Redis Cache (local)                 │
└─────────────────────────────────────────┘
```

### 0.2 Interface REST do Agent

```typescript
/**
 * POST /agent/process
 * Processa uma mensagem de paciente
 */
interface ProcessRequest {
  paciente_id: UUID;
  sessao_id: UUID;
  mensagem: string;
  contexto?: Record<string, any>; // Injetado pela app interna
}

interface ProcessResponse {
  sucesso: boolean;
  resposta_texto: string;
  intenção: string; // 'agendamento', 'cancelamento', etc
  ações_requeridas?: Array<{
    tipo: string; // 'confirmar_agendamento', 'chamar_api', etc
    parametros: Record<string, any>;
  }>;
  dossiê_handoff?: object; // Se vai transferir para humano
  alerta_crise?: { tipo: string; contatos: string[] }; // Se detectada crise
}
```

### 0.3 Fluxo de Integração

```
Paciente envia mensagem
        ↓
App Interna recebe
        ↓
App Interna → GET /api/pacientes/{id}
(recupera contexto do paciente)
        ↓
App Interna → POST /agent/process
(envia mensagem + contexto)
        ↓
Agent LLM processa
(LangGraph + LLM)
        ↓
Agent → GET /api/agendamentos/{paciente_id}
(se precisa de dados)
        ↓
Agent retorna resposta estruturada
        ↓
App Interna processa ações
(confirma agendamento, processa pagamento, etc)
        ↓
App Interna envia resposta ao paciente
```

---

## 1. Camada de Interação (Agent Layer)

### 1.1 LLM + System Prompt Dinâmico

**Objetivo**: Manter uma conversa natural com o paciente, contextualizada e segura.

**Stack**:
- **Framework**: LangGraph (orquestração de fluxos)
- **LLM**: Google Composer 2 (com compatibilidade OpenAI/Claude)
- **Componentes**:
  - **LLM Client**: Interface com Composer 2
  - **System Prompt Manager**: Injeção dinâmica de contexto
  - **Message History Manager**: Manutenção de histórico conversacional

**Fluxo (via LangGraph)**:
```
Mensagem do Paciente
        ↓
[LangGraph Graph Definition]
        ↓
[Node 1] Recuperar Perfil do Paciente
(via API aplicação interna)
        ↓
[Node 2] Construir System Prompt Dinâmico:
    - Dados do paciente (nome, histórico)
    - Persona (clínico vs. comercial)
    - Restrições de segurança
    - Tools disponíveis
        ↓
[Node 3] Intent Detection + Safety Check
(paralelo com LLM)
        ↓
[Node 4] IF Crise:
    → CALL Protocolo Emergência
    ELSE:
    → [Node 5] Chamar Composer 2 com Tool Calling
        ↓
[Node 6] Tool Calling Handler
(executar ações via API interna)
        ↓
Resposta Estruturada (text + tool_results)
```

**Arquitetura LangGraph**:
- Grafo de estados bem definido
- Nodes para cada etapa do fluxo
- Edges com condições (IF/ELSE)
- Suporte a paralelização (safety check)
- Persistência de estado entre mensagens

**Safety Filters**:
- ✅ Apenas responder sobre serviços catalogados
- ✅ Nunca inventar preços
- ✅ Detectar intenções de crise
- ✅ Limitar escopo de respostas médicas

---

### 1.2 Tool Calling (Function Calling)

O LLM é instruído a usar **funções estruturadas** para ações críticas:

```json
{
  "tools": [
    {
      "name": "buscar_disponibilidade",
      "description": "Busca horários disponíveis para um serviço",
      "parameters": {
        "servico_id": "uuid",
        "data_inicio": "YYYY-MM-DD",
        "data_fim": "YYYY-MM-DD",
        "profissional_id": "uuid (opcional)"
      }
    },
    {
      "name": "validar_desconto",
      "description": "Valida elegibilidade para desconto",
      "parameters": {
        "paciente_id": "uuid",
        "servico_id": "uuid",
        "motivo": "string"
      }
    },
    {
      "name": "confirmar_agendamento",
      "description": "Confirma reserva com lock transacional",
      "parameters": {
        "paciente_id": "uuid",
        "servico_id": "uuid",
        "data_hora": "ISO8601",
        "profissional_id": "uuid",
        "dados_adicionais": {
          "cpf": "string (se não existir)",
          "email": "string (se não existir)"
        }
      }
    }
  ]
}
```

**Validações no Backend**:
- Verificar lock temporário
- Validar regras de negócio
- Executar transação ACID
- Retornar protocolo

---

### 1.3 Intent Detection & Crisis Router

**Pipeline de Detecção**:

```
Mensagem Recebida
        ↓
[Análise Paralela]
├─ Detectar Intenção (classification)
│   ├─ Agendamento
│   ├─ Cancelamento
│   ├─ Consulta de Serviço
│   ├─ Reclamação
│   └─ Outro
│
├─ Detectar Risco/Crise (safety check)
│   ├─ Urgência médica
│   ├─ Ideação suicida (saúde mental)
│   ├─ Agressividade/Abuso
│   └─ Outro risco
│
└─ Calcular Confiança (score 0-1)

IF Risco Detectado:
    → INTERROMPER fluxo normal
    → ATIVAR protocolo de emergência
    → ALERTAR equipe clínica
ELSE:
    → Rotear para handler apropriado
```

**Gatilhos de Crise**:
- ⚠️ Menções de "suicídio", "automutilação", "desespero"
- ⚠️ Solicitações explícitas de emergência
- ⚠️ Padrões de comportamento agressivo

---

## 2. Camada de Aplicação (Business Logic Layer)

### 2.1 Service Layer

**Responsabilidade**: Implementar regras de negócio e orquestrar operações.

```typescript
// Pseudocódigo
class AgendamentoService {
  
  async validarDisponibilidade(params): Promise<Slot[]> {
    // Consultar BD para slots livres
    // Validar restrições de profissional
    // Retornar opções ordenadas
  }
  
  async validarDesconto(params): Promise<DescontoResponse> {
    // Aplicar regras parametrizadas
    // Consultar histórico do paciente
    // Retornar limite de desconto ou INELEGÍVEL
  }
  
  async confirmarAgendamento(params): Promise<Agendamento> {
    // [TRANSAÇÃO INICIADA]
    // 1. Validar lock temporário
    // 2. Bloquear slot (INSERT lock)
    // 3. Validar dados obrigatórios (CPF, email)
    // 4. Inserir agendamento
    // 5. Incrementar counter
    // [TRANSAÇÃO FINALIZADA]
    // 6. Gerar protocolo
    // 7. Disparar webhooks (confirmação, lembrete)
    // Retornar confirmação com protocolo
  }
}
```

### 2.2 Data Validation & Rules Engine

**Validações Estritas**:
- ✅ Dados obrigatórios (CPF, e-mail) antes de commit
- ✅ Regras de antecedência para cancelamento
- ✅ Limites de desconto por perfil
- ✅ Restrições de agenda por profissional/especialidade
- ✅ Validação de periodicidade (ex: estética a cada 30 dias)

**Rules Engine (Parametrizado)**:
```json
{
  "descontos": [
    {
      "id": "promo_primeira_visita",
      "condicoes": {
        "primeira_visita": true,
        "especialidade": ["estética", "beleza"]
      },
      "desconto_percentual": 15,
      "validade": "2026-12-31"
    }
  ],
  "cancelamento": {
    "minimo_horas_antecedencia": 24,
    "taxa_cancelamento": 0,
    "regra_especial_saude_mental": "aviso gentil sem taxa"
  }
}
```

---

### 2.3 State Management & Concurrency

**Lock Temporário**:
```
1. Paciente vê horário disponível
2. Backend cria lock (TTL = 5 min)
   ├─ agendamento_id: temp-uuid
   ├─ paciente_id: uuid
   ├─ data_hora: ISO8601
   └─ criado_em: timestamp

3. Paciente confirma:
   ├─ Validar lock ainda ativo
   ├─ Upgrade para agendamento real
   └─ Liberar lock

4. Paciente sai sem confirmar:
   └─ TTL expira → slot fica livre
```

**Controle de Concorrência**:
- ✅ Pessimistic Locking (lock explícito)
- ✅ Ou Optimistic Locking (version numbers)
- ✅ Timeouts configuráveis (default: 5 min)

---

## 3. Camada de Dados (Data Layer)

### 3.1 Schema Simplificado

```sql
-- Entidades Principais

Table Pacientes {
  id UUID PRIMARY KEY
  nome VARCHAR(255)
  cpf VARCHAR(14) UNIQUE (criptografado)
  email VARCHAR(255)
  telefone VARCHAR(20)
  especialidade_preferida VARCHAR(100)
  criado_em TIMESTAMP
  atualizado_em TIMESTAMP
  dados_privados JSONB (criptografado)
  -- saúde mental: máxima privacidade
}

Table Servicos {
  id UUID PRIMARY KEY
  nome VARCHAR(255)
  descricao TEXT
  duracao_minutos INT
  preco_base DECIMAL(10,2)
  categoria VARCHAR(100) -- "estética", "psicologia", etc
  ativo BOOLEAN DEFAULT true
}

Table Agendamentos {
  id UUID PRIMARY KEY
  paciente_id UUID FK
  servico_id UUID FK
  profissional_id UUID FK
  data_hora TIMESTAMP
  status ENUM('pendente', 'confirmado', 'realizado', 'cancelado')
  protocolo VARCHAR(20) UNIQUE
  dados_complementares JSONB
  criado_em TIMESTAMP
  
  UNIQUE(profissional_id, data_hora) -- evita double-booking
}

Table LocksTemporarios {
  id UUID PRIMARY KEY
  agendamento_id UUID FK
  paciente_id UUID FK
  criado_em TIMESTAMP
  expira_em TIMESTAMP (TTL AUTO)
}

Table Descontos {
  id UUID PRIMARY KEY
  agendamento_id UUID FK
  percentual DECIMAL(5,2)
  motivo VARCHAR(100)
  aprovado_por VARCHAR(100) -- admin ou regra automática
  criado_em TIMESTAMP
}

Table Lembretes {
  id UUID PRIMARY KEY
  agendamento_id UUID FK
  tipo ENUM('24h', '48h', 'dia_anterior')
  status ENUM('pendente', 'enviado', 'falha')
  enviado_em TIMESTAMP
}

Table HistoricoInteracoes {
  id UUID PRIMARY KEY
  paciente_id UUID FK
  tipo ENUM('chat', 'agendamento', 'cancelamento', etc)
  payload JSONB -- contexto da interação
  timestamp TIMESTAMP
}
```

### 3.2 Índices e Performance

```sql
-- Índices críticos
CREATE INDEX idx_agendamentos_paciente_data 
  ON Agendamentos(paciente_id, data_hora);

CREATE INDEX idx_agendamentos_profissional_data 
  ON Agendamentos(profissional_id, data_hora);

CREATE INDEX idx_locks_expiracao 
  ON LocksTemporarios(expira_em);

CREATE INDEX idx_lembretes_agendamento_status 
  ON Lembretes(agendamento_id, status);
```

---

## 4. Fluxo End-to-End: Agendamento

```
┌─────────────────────────────────────────────────────────────────┐
│                    PACIENTE: "Quero agendar"                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
          ┌──────────────────────────────────┐
          │  [AGENT LAYER]                   │
          │  • Identificar intenção          │
          │  • Coletar parâmetros            │
          │  • Chamar tool: buscar_slots     │
          └──────────────────┬───────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  [APPLICATION LAYER]                   │
        │  BuscaSlotService:                     │
        │  • Validar especialidade               │
        │  • Consultar BD (Agendamentos, Locks)  │
        │  • Filtrar por disponibilidade         │
        │  • Retornar opções ordenadas           │
        └──────────────────┬─────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │  [DATA LAYER]                                │
    │  SELECT * FROM Agendamentos                  │
    │  WHERE profissional_id = ? AND data BETWEEN │
    │  AND NOT EXISTS (SELECT 1 FROM LocksTemp)   │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼ [Retorna 3 opções]
    ┌──────────────────────────────────────────┐
    │  [AGENT LAYER]                           │
    │  "Encontrei 3 horários. Qual você        │
    │   prefere?"                              │
    │  1) Seg 10:00  2) Seg 14:00  3) Ter 09:00
    └──────────────────┬──────────────────────┘
                       │
                       ▼
        ┌───────────────────────────────┐
        │ PACIENTE: "Quero Seg 14:00"   │
        └───────────────┬───────────────┘
                        │
                        ▼
          ┌─────────────────────────────────┐
          │  [AGENT LAYER]                  │
          │  • Extrair horário              │
          │  • Validar dados obrigatórios   │
          │  • Chamar: confirmar_agendamento
          └──────────────┬──────────────────┘
                         │
                         ▼
    ┌────────────────────────────────────────────┐
    │  [APPLICATION LAYER]                       │
    │  ConfirmarAgendamentoService:              │
    │  [TRANSAÇÃO INICIADA]                      │
    │  • Validar lock ainda ativo                │
    │  • Validar dados (CPF, email)              │
    │  • INSERT agendamento                      │
    │  • DELETE lock                             │
    │  • Gerar protocolo                         │
    │  [TRANSAÇÃO FINALIZADA]                    │
    │  • Disparar webhooks                       │
    │  • Agendar lembretes (workers)             │
    └──────────────┬───────────────────────────┘
                   │
                   ▼
    ┌────────────────────────────────────────┐
    │  [DATA LAYER - CONFIRMAÇÃO]            │
    │  INSERT Agendamentos (...)             │
    │  DELETE LocksTemporarios WHERE id=...  │
    │  INSERT Lembretes (24h, 48h)           │
    └────────────────────────────────────────┘
                   │
                   ▼
    ┌────────────────────────────────────────┐
    │  [WEBHOOKS & WORKERS]                  │
    │  • Enviar SMS/Email confirmação        │
    │  • Agendar notificações                │
    │  • Registrar no histórico              │
    └────────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │  [AGENT LAYER - RESPOSTA]        │
        │  "✅ Agendado com sucesso!       │
        │   Protocolo: #AG-20260613-001    │
        │   Seg, 13 de junho - 14:00"      │
        └──────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │  [PACIENTE]                      │
        │  Recebe confirmação              │
        └──────────────────────────────────┘
```

---

## 5. Padrões de Design

### 5.1 Command Pattern
Cada ação do paciente é convertida em um "Comando" estruturado:
```typescript
interface Command {
  tipo: 'agendamento' | 'cancelamento' | 'consulta_servico';
  paciente_id: UUID;
  parametros: Record<string, any>;
  timestamp: ISO8601;
}
```

### 5.2 Strategy Pattern
Diferentes estratégias por tipo de serviço:
```typescript
interface AgendamentoStrategy {
  validarEligibilidade(): boolean;
  aplicarRegrasEspecificas(): void;
  calcularProximoDisponivel(): DateTime;
}

class AgendamentoEsttica implements AgendamentoStrategy { ... }
class AgendamentoSaudeMental implements AgendamentoStrategy { ... }
```

### 5.3 Observer Pattern
Disparar notificações quando eventos ocorrem:
```typescript
class AgendamentoService extends EventEmitter {
  confirmar() {
    // ...
    this.emit('agendamento:confirmado', { agendamento, paciente });
    // Listeners: EmailService, SMSService, HistoricoService, etc
  }
}
```

---

## 6. Considerações de Segurança

| Aspecto | Estratégia |
|---------|-----------|
| **Dados Sensíveis** | Criptografia em repouso (CPF, email) |
| **Transações** | ACID + locks pessimistas |
| **Autenticação** | OAuth 2.0 ou token JWT |
| **Autorização** | RBAC (paciente, recepcionista, médico, admin) |
| **Auditoria** | Log de todas as alterações críticas |
| **Rate Limiting** | Throttle por paciente para evitar spam |
| **Validação Input** | Sanitização rigorosa antes de persistir |

---

## 7. Escalabilidade

- **Cache**: Redis para slots/preços (TTL curto)
- **Fila de Mensagens**: RabbitMQ ou similar para lembretes
- **Workers**: Múltiplos workers para processar confirmações assincronamente
- **Replicação BD**: Read replicas para consultas pesadas
- **CDN**: Para assets estáticos

---

**Próximo**: Consulte [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md) para detalhes de cada fluxo.

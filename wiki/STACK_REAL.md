# 🔧 Stack Tecnológico Real do AutoCare Agent

**Data de Atualização**: Junho 2026  
**Versão**: 1.0  
**Status**: Confirmado

---

## 📋 Resumo Executivo

O AutoCare Agent **não é um sistema monolítico** independente. É um **microserviço especializado** que fica **atrás de uma aplicação interna existente** e funciona como **consumidor de APIs**.

---

## 🏗️ Arquitetura Real

### Componentes de Alto Nível

```
┌──────────────────────────────────────────────────────────────┐
│       APLICAÇÃO INTERNA (Orquestradora - Dona dos Dados)     │
│  Responsabilidades:                                          │
│  • Receber requisições de múltiplas fontes                  │
│  • Gerenciar persistência (PostgreSQL)                      │
│  • Processar pagamentos                                      │
│  • Distribuir notificações (Email, SMS, Push)               │
│  • Orquestrar chamadas ao Agent LLM                         │
└──────────────┬──────────────────────────────────────────────┘
               │ REST API
               │ POST /agent/process
               ▼
┌──────────────────────────────────────────────────────────────┐
│  AUTOCARE AGENT (Consumidor de APIs - Processador LLM)      │
│  Stack:                                                      │
│  • Python (Linguagem)                                        │
│  • LangGraph (Framework de orquestração)                    │
│  • Google Composer 2 (LLM principal)                        │
│    └─ Compatível com OpenAI/Claude (fallback)              │
│  • Redis (Cache local de contexto)                         │
│                                                             │
│  Responsabilidades:                                         │
│  • Processar conversas via LLM                             │
│  • Extrair intenções (agendamento, cancelamento, etc)      │
│  • Executar Tool Calling (chamadas REST)                   │
│  • Detectar crises (protocolo de emergência)               │
│  • Retornar respostas estruturadas                         │
└──────────────┬──────────────────────────────────────────────┘
               │ REST API
               │ GET /api/pacientes
               │ GET /api/agendamentos
               │ POST /api/pagamentos (etc)
               ▼
    ┌──────────────────────────────┐
    │  Aplicação Interna (APIs)    │
    │  • /api/pacientes            │
    │  • /api/agendamentos         │
    │  • /api/pagamentos           │
    │  • /api/notificacoes         │
    │  • ... (outras rotas)        │
    └──────────────────────────────┘
```

---

## 🛠️ Stack Detalhado

### Backend (Agent LLM)

```json
{
  "linguagem": "Python 3.10+",
  "framework_orquestracao": "LangGraph",
  "llm_principal": "Google Composer 2",
  "llm_fallback": [
    "OpenAI GPT-4 (compatibilidade)",
    "Anthropic Claude (compatibilidade)"
  ],
  "cache_local": "Redis",
  "http_client": "aiohttp ou requests",
  "async": "asyncio",
  "tipo_api": "REST"
}
```

### Aplicação Interna (Existente)

```json
{
  "banco_dados": "PostgreSQL",
  "estado": "Gerenciado internamente",
  "pagamento": "Processado internamente",
  "mensagens": "Queue interna (RabbitMQ, Redis, etc)",
  "notificacoes": "Email, SMS, Push via serviços internos",
  "agent_integration": "REST API client"
}
```

### Dados Persistidos

| Quem Persiste | O Quê | Onde |
|---|---|---|
| **Aplicação Interna** | Pacientes, Agendamentos, Serviços, Preços, Pagamentos | PostgreSQL |
| **Agent LLM** | Contexto de sessão, histórico conversacional | Redis (local) |
| **Agent LLM** | Logs de processamento | Stdout/Logging |

---

## 🔄 Fluxo de Requisição

### Exemplo: Agendamento

```
1. PACIENTE
   └─ "Quero agendar uma limpeza de pele"

2. APLICAÇÃO INTERNA
   └─ POST /agent/process
      {
        "paciente_id": "uuid",
        "sessao_id": "uuid",
        "mensagem": "Quero agendar uma limpeza de pele",
        "contexto": {
          "nome_paciente": "Maria",
          "historico": [...],
          "especialidade_preferida": "estética",
          "...": "..."
        }
      }

3. AGENT LLM (LangGraph + Composer 2)
   └─ [Node 1] Recuperar perfil (contexto já injetado)
   └─ [Node 2] System Prompt + Context Injection
   └─ [Node 3] Intent Detection (em paralelo com LLM)
   └─ [Node 4] IF crise → Emergência ELSE → Processar
   └─ [Node 5] Tool Calling: buscar_disponibilidade
      ├─ Agent faz REST → /api/agendamentos/disponibilidade
      ├─ App Interna retorna slots
   └─ [Node 6] Tool Calling: validar_desconto
      ├─ Agent faz REST → /api/descontos/validar
      ├─ App Interna retorna elegibilidade + percentual
   └─ [Node 7] Retorna resposta estruturada
      {
        "sucesso": true,
        "resposta_texto": "Ótimo! Encontrei 3 horários...",
        "intenção": "agendamento",
        "ações_requeridas": [
          {
            "tipo": "apresentar_opcoes",
            "parametros": {
              "slots": [...]
            }
          }
        ]
      }

4. APLICAÇÃO INTERNA
   └─ Recebe resposta
   └─ Apresenta opções ao paciente
   └─ Aguarda confirmação
   └─ POST /agent/process (nova mensagem)
      {
        "mensagem": "Quero Seg 14:00",
        "...": "..."
      }

5. AGENT LLM (continua conversação)
   └─ Valida seleção
   └─ Oferece desconto
   └─ Aguarda confirmação
   └─ Retorna ação: "confirmar_agendamento"

6. APLICAÇÃO INTERNA
   └─ Executa confirmação
   └─ POST /api/agendamentos/confirmar
      {
        "paciente_id": "...",
        "servico_id": "...",
        "data_hora": "2026-06-16T14:00:00Z",
        "..."
      }
   └─ Processa pagamento
   └─ Envia notificações
   └─ Retorna protocolo ao paciente
```

---

## 🔌 Interface REST do Agent

### Endpoint: POST /agent/process

**Requisição**:
```typescript
interface ProcessRequest {
  paciente_id: UUID;
  sessao_id: UUID;
  mensagem: string;
  contexto?: {
    nome_paciente?: string;
    email?: string;
    telefone?: string;
    cpf?: string;
    especialidade_preferida?: string;
    historico_agendamentos?: Array<{
      id: UUID;
      servico: string;
      data: Date;
      status: string;
    }>;
    total_gasto?: number;
    [key: string]: any;
  };
}
```

**Resposta**:
```typescript
interface ProcessResponse {
  sucesso: boolean;
  resposta_texto: string;
  intenção: string; // 'agendamento', 'cancelamento', 'crise', etc
  ações_requeridas?: Array<{
    tipo: string; // 'confirmar_agendamento', 'chamar_api', etc
    parametros: Record<string, any>;
  }>;
  dossiê_handoff?: {
    motivo: string;
    histórico_resumido: string;
    dados_coletados: Record<string, any>;
  };
  alerta_crise?: {
    tipo: 'suicidio' | 'automutilacao' | 'urgencia' | 'outro';
    contatos_emergencia: string[];
    protocolo: string;
  };
}
```

---

## 🎛️ Orquestração com LangGraph

### Estrutura de Estados

```python
from langgraph.graph import Graph

graph = Graph()

# Nodes (Estados)
graph.add_node("recuperar_perfil", recuperar_perfil_fn)
graph.add_node("intent_detection", intent_detection_fn)
graph.add_node("system_prompt", system_prompt_fn)
graph.add_node("safety_check", safety_check_fn)
graph.add_node("llm_call", llm_call_fn)
graph.add_node("tool_handler", tool_handler_fn)
graph.add_node("crise_handler", crise_handler_fn)
graph.add_node("formatter", formatter_fn)

# Edges (Transições)
graph.add_edge("recuperar_perfil", "system_prompt")
graph.add_edge("system_prompt", ["intent_detection", "safety_check"])
graph.add_conditional_edge(
    "safety_check",
    lambda x: "crise_handler" if x["é_crise"] else "llm_call"
)
graph.add_edge("llm_call", "tool_handler")
graph.add_edge("tool_handler", "formatter")
graph.add_edge(["formatter", "crise_handler"], "end")

# Compilar
app = graph.compile()
```

---

## 📊 Responsabilidades por Camada

| Camada | O Quê | Não Faz |
|--------|-------|---------|
| **Aplicação Interna** | Persistência, Pagamento, Orquestração, Validação de regras críticas | Processamento LLM, Tool Calling direto |
| **Agent LLM** | Conversação, Intent, Tool Calling, Context Injection | Persistência, Processamento de pagamento, Validação crítica |

---

## 🔐 Segurança na Integração

### Dados que NÃO vão para o LLM

```json
{
  "nunca_enviar": [
    "Números de cartão de crédito",
    "Senhas ou tokens",
    "Dados médicos muito sensíveis (apenas resumo)",
    "Informações identificadoras explícitas para busca",
    "Histórico completo (apenas últimas 3 mensagens)"
  ],
  "enviar_apenas_se_necessario": [
    "CPF (em hash)",
    "Email",
    "Telefone"
  ],
  "sempre_enviar": [
    "Nome (ou iniciais)",
    "Especialidade preferida",
    "Histórico resumido de agendamentos",
    "Moeda/localização"
  ]
}
```

### Rate Limiting e Timeouts

```json
{
  "rate_limiting": {
    "por_sessao_minuto": 10,
    "por_ip_minuto": 100,
    "por_paciente_hora": 50
  },
  "timeouts": {
    "agent_process_segundos": 30,
    "tool_call_segundos": 10,
    "total_conversacao_minutos": 60
  },
  "autenticacao": {
    "tipo": "API Key ou JWT",
    "origem": "Aplicação Interna apenas",
    "header": "Authorization: Bearer <token>"
  }
}
```

---

## 🚀 Deployment

### Variáveis de Ambiente (.env)

```env
# LLM
COMPOSER_API_KEY=xxx
LLM_MODEL=composer-pro
FALLBACK_LLM_PROVIDER=openai
FALLBACK_LLM_KEY=xxx

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Aplicação Interna
INTERNAL_APP_BASE_URL=http://localhost:8000
INTERNAL_APP_API_KEY=xxx

# Segurança
JWT_SECRET=xxx
ENCRYPTION_KEY=xxx

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=xxx (opcional)
```

### Deployment Options

```yaml
Docker:
  image: autocare-agent:1.0
  ports:
    - "8001:8000"  # Agent roda na porta 8001
  environment:
    - COMPOSER_API_KEY=${COMPOSER_API_KEY}
    - INTERNAL_APP_BASE_URL=${INTERNAL_APP_BASE_URL}
  depends_on:
    - redis
    - internal-app

Kubernetes:
  deployment:
    replicas: 3
    resources:
      cpu: "500m"
      memory: "1Gi"
  service:
    type: ClusterIP
    port: 8001
```

---

## 📈 Performance

### Benchmarks Esperados

```json
{
  "latency": {
    "intent_detection_ms": 50,
    "llm_call_ms": 2000,
    "tool_call_ms": 500,
    "total_process_ms": 2600
  },
  "throughput": {
    "requisicoes_por_segundo": 10,
    "com_3_replicas": 30
  },
  "cache_hit_rate": 0.70,
  "error_rate": "<0.1%"
}
```

---

## 🔄 Fluxo de Atualização

Se precisar atualizar LLMs ou dependências:

```bash
# 1. Atualizar Composer 2
pip install google-cloud-aiplatform --upgrade

# 2. Testar em staging
pytest tests/

# 3. Deploy gradual (canary)
kubectl set image deployment/autocare-agent \
  autocare-agent=autocare-agent:v1.1

# 4. Monitorar métricas
datadog dashboards
```

---

## 📞 Troubleshooting

### Problema: Agent responde lentamente

**Causa Provável**: Aplicação interna lenta ou Redis sem cache

**Solução**:
- Verificar logs da aplicação interna
- Validar conexão com Redis
- Aumentar timeout do agent

### Problema: Tool Calling falha

**Causa Provável**: Endpoint da aplicação interna indisponível

**Solução**:
- Verificar status da aplicação interna
- Revisar credenciais da API
- Revisar rate limiting

### Problema: Crise não é detectada

**Causa Provável**: Modelo LLM com performance baixa ou keywords não cobertos

**Solução**:
- Revisar lista de gatilhos em REGRAS_NEGOCIO.md
- Aumentar confidence threshold
- Retratar modelo com dados novos

---

## 📚 Referências

- [ARQUITETURA.md](./ARQUITETURA.md) - Detalhes técnicos
- [COMPONENTES.md](./COMPONENTES.md) - APIs e modelos de dados
- [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md) - Fluxos funcionais
- [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md) - Regras de negócio

---

**Versão**: 1.0  
**Data**: Junho 2026  
**Status**: ✅ Confirmado

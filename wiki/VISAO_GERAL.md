# 🎨 VISÃO GERAL - Diagramas e Visualizações

## 1. Arquitetura Geral em Camadas

```
┌──────────────────────────────────────────────────────────────┐
│                      PACIENTE / USUÁRIO                      │
│            (WhatsApp, Web, Mobile App, SMS, Email)           │
└────────────────────────────┬─────────────────────────────────┘
                             │ (Mensagem em linguagem natural)
                             ▼
        ┌────────────────────────────────────────┐
        │    CAMADA DE INTERAÇÃO (Agent Layer)   │
        │  ┌──────────────────────────────────┐  │
        │  │  LLM (Google Composer 2.5)       │  │
        │  │  + System Prompt Dinâmico        │  │
        │  │  + Context Injection             │  │
        │  └──────────────────────────────────┘  │
        │              ▲    ▼                     │
        │  ┌──────────┴──────────┬──────────┐   │
        │  │  Intent   │  Safety  │  Tools   │   │
        │  │ Detection │ Filters  │ Calling  │   │
        │  └──────────┴──────────┴──────────┘   │
        └────────────────────────────────────────┘
                             │ (Function Calls)
                             ▼
    ┌────────────────────────────────────────────────┐
    │  CAMADA DE APLICAÇÃO (Business Logic Layer)   │
    │  ┌──────────────────────────────────────────┐ │
    │  │  Service Layer                           │ │
    │  │  • Agendamento Service                   │ │
    │  │  • Desconto Service                      │ │
    │  │  • Cancelamento Service                  │ │
    │  │  • Validação & Rules Engine              │ │
    │  └──────────────────────────────────────────┘ │
    │              ▲    ▼                            │
    │  ┌──────────────────────────────────────────┐ │
    │  │  Event Emitter / Webhooks                │ │
    │  │  └─ Email Service                        │ │
    │  │  └─ SMS Service                          │ │
    │  │  └─ WhatsApp Service                     │ │
    │  │  └─ Histórico Service                    │ │
    │  └──────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
                             │ (SQL Queries)
                             ▼
        ┌────────────────────────────────────────┐
        │   CAMADA DE DADOS (Data Layer)         │
        │  ┌──────────────────────────────────┐  │
        │  │  PostgreSQL / MongoDB            │  │
        │  │  • Pacientes                     │  │
        │  │  • Agendamentos                  │  │
        │  │  • Serviços                      │  │
        │  │  • Locks Temporários             │  │
        │  │  • Histórico                     │  │
        │  └──────────────────────────────────┘  │
        │              ▲                          │
        │  ┌──────────┴──────────┐              │
        │  │ Cache (Redis)        │              │
        │  │ • Slots              │              │
        │  │ • Preços             │              │
        │  └──────────┬──────────┘              │
        └────────────────────────────────────────┘
```

---

## 2. Fluxo de Agendamento - Visão Simplificada

```
PACIENTE "Quero agendar"
       │
       ▼
AGENT: "Qual serviço?"
       │
       ▼ (LLM extrai intenção)
SERVIÇO: Limpeza de Pele
       │
       ▼ (Tool: buscar_disponibilidade)
BACKEND: SELECT slots livres
       │
       ▼
AGENT: "Qual horário?"
       │ (3 opções)
       │
       ▼
PACIENTE: "Seg 14:00"
       │
       ▼ (Tool: validar_desconto)
BACKEND: 15% OFF? SIM ✓
       │
       ▼
AGENT: "Você ganha 15% OFF!"
       │
       ▼
PACIENTE: "Confirma?"
       │
       ▼
PACIENTE: "SIM!"
       │
       ▼ (Tool: confirmar_agendamento)
BACKEND:
  [TRANSAÇÃO INICIADA]
  • Validar lock
  • Criar agendamento
  • Criar lembretes
  [TRANSAÇÃO FINALIZADA]
       │
       ▼
AGENT: "✅ CONFIRMADO!"
       │ Protocolo: AG-20260616-001
       │ Seg, 16/jun - 14:00
       │
       ▼
WEBHOOKS:
  • Email confirmação
  • SMS confirmação
  • Agenda remota atualizada
       │
       ▼
PACIENTE: "Agendamento confirmado!"
```

---

## 3. Matriz de Responsabilidades

```
┌──────────────────┬──────────────┬──────────────┬──────────────┐
│ Atividade        │ Agent (LLM)  │ Backend      │ Banco de     │
│                  │              │              │ Dados        │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Conversa Natural │ ✅ Sim       │ Não          │ Não          │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Entender Intent  │ ✅ Sim       │ Não          │ Não          │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Injetar Contexto │ ✅ Sim       │ Prepara      │ ✅ Sim       │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Validar Dados    │ Sugere       │ ✅ Valida    │ Não          │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Calcular Preço   │ Nunca!       │ ✅ Sempre    │ ✅ Armazena  │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Lock Slot        │ Não          │ ✅ Sim       │ ✅ Sim       │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Confirmar Agenda │ Não          │ ✅ Valida    │ ✅ Persiste  │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Enviar Email     │ Não          │ ✅ Dispara   │ Não          │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Criar Histórico  │ Não          │ ✅ Registra  │ ✅ Armazena  │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Detectar Crise   │ ✅ Sim       │ ✅ Valida    │ Não          │
└──────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 4. Estados de um Agendamento

```
                    ┌─────────────┐
                    │   PENDENTE  │
                    └──────┬──────┘
                           │
                    ┌──────▼────────┐
                    │  PAGAMENTO    │
                    │  (Webhook)    │
                    └──────┬────────┘
                           │
                    ┌──────▼──────────┐
                    │  CONFIRMADO     │
                    └──────┬──────────┘
                           │
                    ┌──────▼───────────┐
                    │  REALIZADO       │
                    │  (Após 48h)      │
                    └──────┬───────────┘
                           │
                    ┌──────▼────────────┐
                    │  NPS/FOLLOW-UP    │
                    └───────────────────┘

           ALT (Cancelamento em qualquer estado)
                           │
                    ┌──────▼──────────┐
                    │  CANCELADO      │
                    │  (Reembolso)    │
                    └─────────────────┘
```

---

## 5. Especialidades e Personas

```
┌──────────────────────────────────────┬──────────────────────────┐
│           ESPECIALIDADE              │    PERSONA DO AGENT      │
├──────────────────────────────────────┼──────────────────────────┤
│                                      │                          │
│  🧠 Psicologia / Psiquiatria         │  Clínico + Acolhedor    │
│  └─ Máxima privacidade              │  ├─ Empático             │
│  └─ Sem taxa cancelamento           │  ├─ Cuidadoso            │
│  └─ Triagem de risco                │  └─ Detecção de crises  │
│                                      │                          │
├──────────────────────────────────────┼──────────────────────────┤
│                                      │                          │
│  💅 Estética / Beleza               │  Comercial + Entusiasta │
│  └─ Promoções agressivas           │  ├─ Entusiasmado        │
│  └─ Cross-selling                  │  ├─ Recomendativo       │
│  └─ Combos de serviços             │  └─ Orientado a venda   │
│                                      │                          │
├──────────────────────────────────────┼──────────────────────────┤
│                                      │                          │
│  💇 Salão / Cabelo                  │  Amigável + Prático    │
│  └─ Fidelização                     │  ├─ Jovial              │
│  └─ Pacotes                         │  ├─ Direto              │
│  └─ Recorrência rápida              │  └─ Eficiente           │
│                                      │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 6. Ciclo de Vida da Conversa do Paciente

```
          [Entrada]
             │
             ▼
    ┌────────────────────┐
    │ 1. ACOLHIMENTO     │
    │ Identificar paciente│
    │ Injetar contexto   │
    │ Persona roteamento │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │ 2. INTENÇÃO        │
    │ Entender o que     │
    │ paciente quer      │
    └────────┬───────────┘
             │
      ┌──────┴──────┬──────────────┬──────────────┐
      │             │              │              │
      ▼             ▼              ▼              ▼
 [Agendamento] [Consulta]  [Cancelamento]   [Crise?]
      │             │              │              │
      └──────┬──────┴──────────────┴──────────────┘
             │
             ▼
    ┌────────────────────┐
    │ 3. RESOLUÇÃO       │
    │ Tool Calling       │
    │ Validações         │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │ 4. CONFIRMAÇÃO     │
    │ Resumir resultado  │
    │ Próximos passos    │
    └────────┬───────────┘
             │
      ┌──────┴─────────────────┐
      │                        │
   [Sucesso]            [Falha/Incerteza]
      │                        │
      ▼                        ▼
  [FIM]               ┌─────────────────┐
                      │ 5. DEFLEXÃO     │
                      │ Tentar resolver │
                      │ Senão, handoff  │
                      └────────┬────────┘
                               │
                               ▼
                        [Transferência]
                        ou
                        [FIM com falha]
```

---

## 7. Stack Tecnológico Recomendado

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (Cliente)                        │
│  React/Vue.js + Tailwind + TypeScript                        │
│  (Web, Mobile com React Native)                              │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTPS/REST
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                    BACKEND (API Layer)                       │
│  Node.js + Express  ou  Python + FastAPI  ou  .NET          │
│  ├─ Servidor API REST                                       │
│  ├─ Autenticação JWT/OAuth                                  │
│  ├─ Validação de Dados                                      │
│  └─ Integração LLM / Payment Gateway                        │
└────────────┬───────────────────────────┬────────────────────┘
             │                           │
             │                           │
    ┌────────▼────────┐      ┌───────────▼──────────┐
    │ BANCO PRINCIPAL │      │  SERVIÇOS EXTERNOS  │
    │ PostgreSQL      │      │                      │
    │ ├─ Pacientes   │      │ ├─ Composer 2.5 API  │
    │ ├─ Agendamentos│      │ ├─ Stripe            │
    │ ├─ Locks       │      │ ├─ MercadoPago       │
    │ ├─ Serviços    │      │ ├─ Twilio (SMS)      │
    │ └─ Histórico   │      │ ├─ SendGrid (Email)  │
    │                │      │ ├─ Firebase Push     │
    │ Indices:       │      │ └─ Whatsapp API      │
    │ ├─ paciente_id │      │                      │
    │ ├─ agenda_data │      │ CACHE                │
    │ └─ locks_ttl   │      │ Redis                │
    └────────────────┘      │ ├─ Slots             │
                            │ ├─ Preços            │
                            │ └─ Sessions          │
                            └─────────────────────┘

    ┌─────────────────────────────────────────────┐
    │          MESSAGE QUEUE / WORKERS            │
    │  RabbitMQ / Redis Queue / Bull              │
    │  ├─ Lembretes (24h, 48h)                   │
    │  ├─ Confirmações de pagamento              │
    │  ├─ Notificações                           │
    │  └─ Processamento assíncrono               │
    └─────────────────────────────────────────────┘

    ┌──────────────────────────────────────────┐
    │       LOGGING & MONITORING               │
    │  ├─ ELK Stack / Datadog / CloudWatch    │
    │  ├─ Sentry (Error Tracking)             │
    │  └─ Prometheus (Metrics)                │
    └──────────────────────────────────────────┘
```

---

## 8. Matriz de Risco

```
┌──────────────────┬────────┬────────────────────────────────────┐
│ Componente       │ Risco  │ Mitigação                          │
├──────────────────┼────────┼────────────────────────────────────┤
│ Agendamento      │ 🔴 Alt │ • Lock temporário (5 min)         │
│ (Double-Booking) │        │ • Transação ACID                  │
│                  │        │ • Validação antes de commit       │
├──────────────────┼────────┼────────────────────────────────────┤
│ Pagamento        │ 🔴 Alt │ • Webhook do gateway              │
│ (Não processado) │        │ • Retry automático                │
│                  │        │ • Auditoria                       │
├──────────────────┼────────┼────────────────────────────────────┤
│ Dados Sensíveis  │ 🔴 Alt │ • Criptografia AES-256            │
│ (Vazamento)      │        │ • HTTPS/TLS                       │
│                  │        │ • Rate limiting                   │
├──────────────────┼────────┼────────────────────────────────────┤
│ Crise Médica     │ 🔴 Alt │ • Detecção automática             │
│ (Não detectada)  │        │ • Contatos de emergência          │
│                  │        │ • Alerta imediato à equipe        │
├──────────────────┼────────┼────────────────────────────────────┤
│ LLM Alucinação   │ 🟠 Alto│ • RAG (banco de dados)            │
│ (Info incorreta) │        │ • Safety filters                  │
│                  │        │ • Tool calling obrigatório       │
├──────────────────┼────────┼────────────────────────────────────┤
│ Downtime BD      │ 🟠 Alto│ • Replicas (HA)                   │
│                  │        │ • Backups automáticos             │
│                  │        │ • Failover automático             │
├──────────────────┼────────┼────────────────────────────────────┤
│ Performance      │ 🟡 Médio│ • Índices otimizados              │
│ (Lentidão)       │        │ • Cache Redis                     │
│                  │        │ • Paginação                       │
└──────────────────┴────────┴────────────────────────────────────┘
```

---

## 9. Diagrama de Transições de Estado

```
                   ┌─────────────┐
                   │   NOVO      │
                   └──────┬──────┘
                          │ (Paciente existe)
                          ▼
                   ┌─────────────┐
            ┌──────│   ATIVO     │◄─────────┐
            │      └──────┬──────┘          │
            │             │ (No-show x3)    │
            │      ┌──────▼──────────┐      │
            │      │  INATIVO        │      │
            │      │  (Usuário)      │      │
            │      └──────┬──────────┘      │
            │             │                 │
            │      ┌──────▼──────────┐      │
            │      │  BANIDO         │      │
            │      │  (7 dias auto)  │      │
            │      └──────┬──────────┘      │
            │             │ (7 dias passa) │
            └─────────────┬─────────────────┘
                          │
                          ▼
            ┌──────────────────────┐
            │  DELETADO (Soft Del) │
            └──────────────────────┘
```

---

## 10. Casos de Uso Críticos

```
┌─────────────────────────────────────────────────────────────┐
│ CASO 1: Agendamento Bem-Sucedido                           │
├─────────────────────────────────────────────────────────────┤
│ Ator: Paciente                                              │
│ Pré-condição: Paciente ativo, serviço disponível           │
│ Fluxo:                                                      │
│  1. Paciente solicita agendamento                          │
│  2. Agent busca disponibilidade                            │
│  3. Agent oferece 3 opções                                 │
│  4. Paciente escolhe uma                                   │
│  5. Agent valida elegibilidade para desconto               │
│  6. Paciente confirma                                      │
│  7. Backend confirma com lock                              │
│  8. Paciente recebe protocolo                              │
│ Pós-condição: Agendamento criado, lembretes agendados     │
│ Critério de Sucesso: RF09-12 implementado ✓               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CASO 2: Detecção de Crise                                  │
├─────────────────────────────────────────────────────────────┤
│ Ator: Paciente (Saúde Mental)                              │
│ Pré-condição: Paciente em risco (suicidio, automutilação) │
│ Fluxo:                                                      │
│  1. Paciente escreve "quero me matar"                      │
│  2. Agent detecta intenção crítica                         │
│  3. Agent interrompe fluxo normal                          │
│  4. Agent oferece contatos de emergência (CVV, SAMU)      │
│  5. Backend dispara webhook para equipe                    │
│  6. Equipe clínica toma atendimento                        │
│ Pós-condição: Alerta gerado, contatos enviados            │
│ Critério de Sucesso: RF19-20 implementado ✓               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CASO 3: Cancelamento com Antecedência                      │
├─────────────────────────────────────────────────────────────┤
│ Ator: Paciente                                              │
│ Pré-condição: Agendamento confirmado, 24h+ antes          │
│ Fluxo:                                                      │
│  1. Paciente solicita cancelamento                         │
│  2. Agent valida antecedência (✓ 24h+)                     │
│  3. Agent informa: sem taxa, 100% reembolso               │
│  4. Paciente confirma cancelamento                         │
│  5. Backend cancela e agenda reembolso                     │
│  6. Backend libera slot para fila de espera                │
│ Pós-condição: Agendamento cancelado, slot liberado        │
│ Critério de Sucesso: RF13-15 implementado ✓               │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. Checklist de Implementação

```
FASE 1: Setup Infrastructure
  ☐ PostgreSQL configurado
  ☐ Redis configurado
  ☐ RabbitMQ/Bull configurado
  ☐ Variáveis de ambiente

FASE 2: Database & Models
  ☐ Schema criado
  ☐ Índices aplicados
  ☐ Migrations pronta

FASE 3: Backend APIs
  ☐ Endpoints CRUD
  ☐ Autenticação
  ☐ Validações
  ☐ Rules Engine

FASE 4: Transações Críticas
  ☐ Lock temporário
  ☐ Agendamento (ACID)
  ☐ Cancelamento
  ☐ Pagamento

FASE 5: Agent Integration
  ☐ LLM Client
  ☐ System Prompt
  ☐ Tool Calling
  ☐ Intent Detection

FASE 6: Safety & Security
  ☐ Criptografia dados
  ☐ Rate Limiting
  ☐ Auditoria
  ☐ Crisis Detection

FASE 7: External Integrations
  ☐ Payment Gateway
  ☐ Email Service
  ☐ SMS Service
  ☐ Push Notifications

FASE 8: Testing & QA
  ☐ Testes unitários
  ☐ Testes de integração
  ☐ Testes de carga
  ☐ Testes de segurança

FASE 9: Monitoring & Logs
  ☐ Logging estruturado
  ☐ Error tracking
  ☐ Metrics
  ☐ Alertas

FASE 10: Deploy & Documentation
  ☐ Documentação de deploy
  ☐ Runbook de operações
  ☐ Treinamento da equipe
```

---

**Para mais detalhes**, consulte:
- [ARQUITETURA.md](./ARQUITETURA.md)
- [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md)
- [COMPONENTES.md](./COMPONENTES.md)

**Versão**: 1.0 | **Data**: Junho 2026

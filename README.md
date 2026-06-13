# 🏥 AutoCare Agent - Sistema de Agente Autônomo para Clínicas

## Visão Geral

O **AutoCare Agent** é um sistema inteligente baseado em IA (LLM) projetado para gerenciar o atendimento, agendamento e experiência do paciente em clínicas de saúde, psicologia, psiquiatria e estética.

### 🎯 Objetivo Principal

Automatizar e otimizar o atendimento ao paciente através de:
- **Acolhimento inteligente** com contexto personalizado
- **Agendamento inteligente** com gestão de slots e concorrência
- **Suporte adaptativo** com diferentes tons de voz conforme a especialidade
- **Deflexão suave** para atendimento humano quando necessário
- **Conversão otimizada** com motor de descontos e cross-selling

---

## 🏢 Domínios Atendidos

- **Saúde Mental**: Psicologia, Psiquiatria (Tom clínico e acolhedor)
- **Estética e Beleza**: Salão de Beleza (Tom comercial e entusiástico)
- **Outros Serviços Médicos e de Bem-estar**

---

## 📊 Arquitetura em Alto Nível

```
┌─────────────────────────────────────────────────────────────┐
│            APLICAÇÃO INTERNA (Orquestradora)                │
│  • Recebe requests de múltiplas fontes                       │
│  • Gerencia persistência, pagamentos, notificações         │
│  • Orquestra chamadas ao Agent via REST                     │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│   AGENTE AUTÔNOMO LLM (Backend - Python + LangGraph)       │
│  • Google Composer 2 (OpenAI/Claude compatible)            │
│  • System Prompt Dinâmico                                   │
│  • Injeção de Contexto do Paciente                          │
│  • Roteamento de Persona                                    │
│  • Detecção de Intenções & Crises                          │
│  • Redis Cache (contexto de sessão)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐    ┌────────┐     ┌────────┐
    │ Tools  │    │ Safety │     │Handlers│
    │(REST)  │    │Filters │     │(Fallback)
    └────────┘    └────────┘     └────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │ REST
                         ▼
    ┌────────────────────────────────────┐
    │   Aplicação Interna (APIs)         │
    │  • PostgreSQL (estado crítico)      │
    │  • Payment Processor                │
    │  • Messaging Queue                  │
    └────────────────────────────────────┘
```

### ⚠️ Nota Importante sobre Arquitetura

**O AutoCare Agent NÃO é uma aplicação monolítica**. Ele é um **microser viço especializado em IA**:

1. **Aplicação Interna**: Funciona como orquestradora central
   - Recebe requisições de múltiplas fontes (pacientes, web, mobile, etc)
   - Gerencia estado, persistência crítica, pagamentos e notificações
   - Mantém a lógica complexa de negócio em nível de banco de dados

2. **AutoCare Agent**: Processa conversas via LLM
   - Recebe requisições REST da aplicação interna com contexto injetado
   - Executa orquestração de fluxos via LangGraph
   - Chama APIs da aplicação interna para dados e ações
   - Retorna respostas estruturadas (texto + ações requeridas)
   - Não persiste dados diretamente no BD

3. **Fluxo de Integração**:
```
Paciente → App Interna → Agent LLM → App Interna → Paciente
         (recebe)      (processa)    (persiste)   (responde)
```

---

## 🔄 Fluxos Principais

| # | Fluxo | Descrição |
|---|-------|-----------|
| 1️⃣ | **Acolhimento e Triagem** | Identificação do paciente e injeção de contexto |
| 2️⃣ | **Base de Conhecimento** | RAG/APIs para consultar procedimentos e preços |
| 3️⃣ | **Negociação e Descontos** | Validação e oferecimento de descontos |
| 4️⃣ | **Agendamento** | Core business: reserva com lock transacional |
| 5️⃣ | **Self-Service** | Gerenciamento de agendamentos pelo paciente |
| 6️⃣ | **Handoff Inteligente** | Transbordo para atendimento humano |
| 7️⃣ | **Detecção de Crise** | Interceptação de urgências médicas |
| 8️⃣ | **Confirmação Ativa** | Lembretes proativos pré-agendamento |
| 9️⃣ | **Fila de Espera** | Waitlist para horários indisponíveis |
| 🔟 | **Agendamento Múltiplo** | Cross-selling e orquestração de profissionais |
| 1️⃣1️⃣ | **Cobrança** | Integração com payment gateway |
| 1️⃣2️⃣ | **Multimodalidade** | Suporte a imagens e documentos |

---

## 🔐 Princípios Arquiteturais

### 1. **Separação de Responsabilidades**
- **LLM**: Raciocínio natural, conversação, sugestões
- **Backend**: Regras estritas, transações, estado
- **Tools**: Interfaces padronizadas para consultas

### 2. **Segurança de Dados**
- Pacientes sensíveis (saúde mental) ⟹ máxima privacidade
- Dados críticos (preços, descontos) ⟹ nunca no LLM
- Detecção ativa de risco/crise ⟹ imediata escalonagem

### 3. **Consistência Transacional**
- Locks temporários para evitar double-booking
- Validações de estado antes de commit
- Rollback automático em caso de falha

### 4. **Experiência Adaptativa**
- Persona por especialidade (clínico vs. comercial)
- Histórico e preferências do paciente injetados
- Tentativa de resolução antes de handoff

---

## 📚 Documentação Estruturada

Para entender como o sistema funciona em detalhe, consulte:

1. **[STACK_REAL.md](./wiki/STACK_REAL.md)** - Stack tecnológico + integração com aplicação interna ⭐ **COMECE AQUI**
2. **[ARQUITETURA.md](./wiki/ARQUITETURA.md)** - Componentes técnicos e padrões
3. **[FLUXOS_PRINCIPAIS.md](./wiki/FLUXOS_PRINCIPAIS.md)** - Detalhamento de cada fluxo com sequências
4. **[REGRAS_NEGOCIO.md](./wiki/REGRAS_NEGOCIO.md)** - Todas as regras de negócio e validações
5. **[COMPONENTES.md](./wiki/COMPONENTES.md)** - Estrutura de APIs, dados e modelos
6. **[GLOSSARIO.md](./wiki/GLOSSARIO.md)** - Termos técnicos e de negócio

---

## 🚀 Como Começar

### Para Técnicos (Desenvolvedores)
1. Leia **[ARQUITETURA.md](./wiki/ARQUITETURA.md)** para entender a estrutura
2. Estude **[COMPONENTES.md](./wiki/COMPONENTES.md)** para conhecer as APIs
3. Analise **[FLUXOS_PRINCIPAIS.md](./wiki/FLUXOS_PRINCIPAIS.md)** para os detalhes de implementação

### Para Gestores e Stakeholders
1. Comece com **[REGRAS_NEGOCIO.md](./wiki/REGRAS_NEGOCIO.md)**
2. Consulte **[FLUXOS_PRINCIPAIS.md](./wiki/FLUXOS_PRINCIPAIS.md)** para fluxos visuais
3. Use **[GLOSSARIO.md](./wiki/GLOSSARIO.md)** para termos

---

## 📋 Requisitos Funcionais Resumidos

✅ RF01-RF32: Consulte o documento completo em [FLUXOS_PRINCIPAIS.md](./wiki/FLUXOS_PRINCIPAIS.md)

- **Acolhimento**: RF01-03
- **Base de Conhecimento**: RF04-06
- **Negociação**: RF07-08
- **Agendamento**: RF09-12
- **Self-Service**: RF13-15
- **Handoff**: RF16-18
- **Detecção de Crise**: RF19-20
- **Confirmação**: RF21-23
- **Waitlist**: RF24-25
- **Cross-Selling**: RF26-27
- **Cobrança**: RF28-29
- **Pós-Atendimento**: RF30
- **Multimodalidade**: RF31-32

---

## 🔗 Stack Tecnológico

### Componentes Principais
- **LLM**: Google Composer 2 (com compatibilidade OpenAI/Claude)
- **Orquestração**: LangGraph
- **Backend**: Python
- **Banco de Dados**: PostgreSQL
- **APIs**: REST

### Integração com Aplicação Interna
- **Payment Gateway**: Chamada à aplicação interna via API
- **Messaging**: Recepção de requests da aplicação interna
- **Broker**: Aplicação interna atua como orquestradora central
- **Comunicação**: REST com polling/webhooks

### Nota Arquitetural
O **AutoCare Agent roda atrás de uma aplicação interna existente** que:
- Recebe requisições de múltiplas fontes
- Orquestra chamadas ao agent via API REST
- Gerencia estado, persistência e transações críticas
- Processa pagamentos internamente
- Distribui notificações via messaging interno

---

## 📞 Suporte

Para dúvidas sobre a documentação, consulte o [GLOSSARIO.md](./wiki/GLOSSARIO.md) ou entre em contato com o time de desenvolvimento.

---

**Versão**: 1.0  
**Data**: Junho 2026  
**Status**: Pronto para Implementação

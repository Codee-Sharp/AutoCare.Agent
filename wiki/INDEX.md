# 📑 ÍNDICE E GUIA DE LEITURA

## 📚 Documentação Completa do AutoCare Agent

Bem-vindo à documentação técnica e de negócios do **AutoCare Agent**! Este índice ajuda você a encontrar exatamente o que precisa.

---

## 🚀 Comece Por Aqui

### Para Entender Rapidamente (10 minutos)
1. 📖 [README.md](../README.md) - Visão geral do projeto
2. 📋 [GLOSSARIO.md](./GLOSSARIO.md) - Entender termos-chave

### Para Aprender Completamente (2 horas)
1. 📖 [README.md](../README.md)
2. 📊 [FLUXOS_PRINCIPAIS.md](#fluxos_principais) - Ver visual dos fluxos
3. 🏗️ [ARQUITETURA.md](#arquitetura) - Entender estrutura
4. 📋 [REGRAS_NEGOCIO.md](#regras_negocio) - Conhecer as regras

### Para Implementar (4+ horas)
1. 🏗️ [ARQUITETURA.md](#arquitetura)
2. 🔧 [COMPONENTES.md](#componentes) - APIs e modelos
3. 📊 [FLUXOS_PRINCIPAIS.md](#fluxos_principais) - Sequência detalhada
4. 📋 [REGRAS_NEGOCIO.md](#regras_negocio) - Validações

---

## 🎯 Guia Por Persona

### 👤 **Você é um Paciente / Usuário Leigo**

**Objetivo**: Entender como a aplicação funciona do seu ponto de vista

**Leitura Recomendada** (15 minutos):
1. [README.md - Visão Geral](../README.md#-visão-geral)
2. [FLUXOS_PRINCIPAIS.md - Agendamento](./FLUXOS_PRINCIPAIS.md#fluxo-4-agendamento-rf09-12--critical)
3. [GLOSSARIO.md - Termos de Negócio](./GLOSSARIO.md#termos-de-negócio)

**Resumo do que você precisa saber**:
- ✅ Como agendar um horário
- ✅ Como cancelar com segurança
- ✅ Quanto você economiza com descontos
- ✅ Como confirmar um agendamento
- ✅ Quem entrar em contato em caso de crise

---

### 🏥 **Você é Gestor / Stakeholder da Clínica**

**Objetivo**: Entender a estratégia de negócio e os ganhos do sistema

**Leitura Recomendada** (45 minutos):
1. [README.md - Completo](../README.md)
2. [FLUXOS_PRINCIPAIS.md - Todos os fluxos](./FLUXOS_PRINCIPAIS.md)
3. [REGRAS_NEGOCIO.md - Políticas e Descontos](./REGRAS_NEGOCIO.md#3-regras-de-desconto)
4. [GLOSSARIO.md - Termos de Negócio](./GLOSSARIO.md#termos-de-negócio)

**Resumo do que você precisa saber**:
- ✅ Como o agente aumenta agendamentos
- ✅ Estratégia de descontos e cross-selling
- ✅ Redução de no-shows com lembretes
- ✅ Detecção de crises em saúde mental
- ✅ Integração com payment gateway
- ✅ ROI esperado

---

### 👨‍💼 **Você é Recepcionista / Atendente**

**Objetivo**: Entender como o sistema me ajuda e quando entra em ação

**Leitura Recomendada** (30 minutos):
1. [README.md - Componentes](../README.md#-stack-tecnológico-esperado)
2. [FLUXOS_PRINCIPAIS.md - Fluxos 6, 7, 8](./FLUXOS_PRINCIPAIS.md#fluxo-6-handoff-inteligente-rf16-18)
3. [GLOSSARIO.md - Termos para Atendentes](./GLOSSARIO.md#se-você-é-um-recepcionista-atendente)

**Resumo do que você precisa saber**:
- ✅ Quais são meus alertas de atendimento
- ✅ Como acessar o dossiê do chat
- ✅ Protocolo de crise e contatos de emergência
- ✅ Como confirmar pagamentos
- ✅ Dashboard de agendamentos

---

### 👨‍💻 **Você é Desenvolvedor Backend**

**Objetivo**: Implementar as APIs e lógica de negócio

**Leitura Recomendada** (3+ horas):
1. [ARQUITETURA.md - Completo](./ARQUITETURA.md)
2. [COMPONENTES.md - APIs e Modelos](./COMPONENTES.md)
3. [FLUXOS_PRINCIPAIS.md - Especialmente Agendamento](./FLUXOS_PRINCIPAIS.md#fluxo-4-agendamento-rf09-12--critical)
4. [REGRAS_NEGOCIO.md - Validações](./REGRAS_NEGOCIO.md)
5. [GLOSSARIO.md - Termos Técnicos](./GLOSSARIO.md#termos-técnicos)

**Checklist de Implementação**:
- ✅ Setup BD (PostgreSQL/MongoDB)
- ✅ Modelos de dados (Paciente, Agendamento, etc)
- ✅ APIs REST (CRUD operations)
- ✅ Sistema de Lock (concorrência)
- ✅ Transações ACID
- ✅ Event Emitters / Webhooks
- ✅ Validações e Rules Engine
- ✅ Integração Payment Gateway
- ✅ Criptografia de dados sensíveis
- ✅ Rate Limiting e Segurança

**Stack Recomendado**:
- Node.js + Express ou Python + FastAPI
- PostgreSQL com indexes otimizados
- Redis para cache de slots
- RabbitMQ para fila de mensagens
- Stripe/MercadoPago para pagamentos

---

### 🤖 **Você é Especialista em IA / Agente**

**Objetivo**: Implementar o LLM e orquestração do agente

**Leitura Recomendada** (2+ horas):
1. [ARQUITETURA.md - Camada de Interação](./ARQUITETURA.md#1-camada-de-interação-agent-layer)
2. [COMPONENTES.md - Tools do Agent](./COMPONENTES.md#4-tools-do-agent)
3. [FLUXOS_PRINCIPAIS.md - Fluxo 1, 6, 7](./FLUXOS_PRINCIPAIS.md#fluxo-1-acolhimento-e-triagem-rf01-03)
4. [GLOSSARIO.md - Termos de IA](./GLOSSARIO.md#termos-técnicos)

**Checklist de Implementação**:
- ✅ Integração com LLM (OpenAI/Claude)
- ✅ System Prompt dinâmico + context injection
- ✅ Tool Calling implementation
- ✅ Intent detection + classification
- ✅ Crisis detection & safety filters
- ✅ Persona roteamento por especialidade
- ✅ Message history management
- ✅ Deflexão suave (fallback handling)
- ✅ Dossier generation para handoff

**Frameworks Recomendados**:
- LangChain / AutoGen / Custom implementation
- OpenAI GPT-4 ou Anthropic Claude
- Vector DB para RAG (Pinecone, Weaviate, etc)

---

### 🔒 **Você é Especialista em Segurança**

**Objetivo**: Garantir proteção de dados e compliance

**Leitura Recomendada** (1+ horas):
1. [ARQUITETURA.md - Considerações de Segurança](./ARQUITETURA.md#6-considerações-de-segurança)
2. [REGRAS_NEGOCIO.md - Regras de Segurança](./REGRAS_NEGOCIO.md#7-regras-de-segurança)
3. [COMPONENTES.md - Modelos de Dados](./COMPONENTES.md#1-modelos-de-dados)
4. [GLOSSARIO.md - Termos de Segurança](./GLOSSARIO.md#termos-de-segurança)

**Checklist de Segurança**:
- ✅ Criptografia em repouso (AES-256)
- ✅ Criptografia em trânsito (TLS/HTTPS)
- ✅ Autenticação (OAuth 2.0 ou JWT)
- ✅ Autorização (RBAC)
- ✅ Rate Limiting
- ✅ Detecção de anomalias
- ✅ Auditoria de acesso
- ✅ Proteção de dados sensíveis (CPF, email)
- ✅ GDPR/LGPD compliance
- ✅ Sanitização de inputs

---

### 🎨 **Você é Designer / Developer Frontend**

**Objetivo**: Criar interface intuitiva para agendamentos

**Leitura Recomendada** (1 hora):
1. [FLUXOS_PRINCIPAIS.md - Visão geral dos fluxos](./FLUXOS_PRINCIPAIS.md)
2. [COMPONENTES.md - APIs do Backend](./COMPONENTES.md#2-apis-do-backend)
3. [GLOSSARIO.md - Termos de UI/UX](./GLOSSARIO.md#termos-de-interface-de-usuário)

**Checklist de Interface**:
- ✅ Busca de disponibilidade (calendário)
- ✅ Seleção de serviço
- ✅ Validação de dados
- ✅ Confirmação com lock visual
- ✅ Exibição de descontos
- ✅ Pagamento integrado
- ✅ Dashboard de agendamentos
- ✅ Notificações (toast/alerts)
- ✅ Responsivo (mobile-first)

**Stack Recomendado**:
- React / Vue.js / Next.js
- TypeScript para type safety
- Tailwind CSS para styling
- React Query para data fetching
- Stripe/MercadoPago SDK

---

## 📄 Estrutura Completa da Documentação

### 📖 [README.md](../README.md)
**Visão geral do projeto**
- Objetivo principal
- Domínios atendidos
- Arquitetura em alto nível
- Fluxos principais
- Princípios arquiteturais
- Stack tecnológico

### 🏗️ [ARQUITETURA.md](./ARQUITETURA.md)
**Estrutura técnica detalhada**
- Camada de Interação (LLM + Agent)
- Camada de Aplicação (Business Logic)
- Camada de Dados (Persistência)
- Fluxo end-to-end de agendamento
- Padrões de design
- Segurança
- Escalabilidade

### 📊 [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md)
**Descrição detalhada de cada fluxo**
- Acolhimento e Triagem (RF01-03)
- Base de Conhecimento (RF04-06)
- Negociação e Descontos (RF07-08)
- Agendamento (RF09-12) ⭐
- Self-Service (RF13-15)
- Handoff Inteligente (RF16-18)
- Detecção de Crise (RF19-20) ⭐
- Confirmação Ativa (RF21-23)
- Fila de Espera (RF24-25)
- Cross-Selling (RF26-27)
- Cobrança (RF28-29)
- Multimodalidade (RF31-32)

### 📋 [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md)
**Regras parametrizadas e políticas**
- Regras de agendamento
- Regras de cancelamento
- Regras de desconto
- Regras de disponibilidade
- Regras de validação
- Regras de cobrança
- Regras de segurança
- Regras por especialidade
- Tabela de referência rápida

### 🔧 [COMPONENTES.md](./COMPONENTES.md)
**Interfaces, APIs e modelos de dados**
- Modelos de dados (Paciente, Agendamento, Serviço, etc)
- APIs do Backend (endpoints REST)
- Estrutura de eventos
- Tools do Agent (Function Calling)
- Response patterns

### 📖 [GLOSSARIO.md](./GLOSSARIO.md)
**Dicionário completo de termos**
- Termos de negócio
- Termos técnicos
- Termos de domínio (saúde)
- Abreviações
- Guia por persona
- FAQ (Perguntas Frequentes)

### 📑 [INDEX.md](./INDEX.md) (Este arquivo)
**Guia de navegação da documentação**

---

## 🔍 Encontre Rapidamente

### Buscar por Palavra-Chave

| Interesse | Arquivo |
|-----------|---------|
| **Agendamento** | [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md#fluxo-4) |
| **Cancelamento** | [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md#fluxo-5) |
| **Desconto** | [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md#fluxo-3) e [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md#3) |
| **Crise/Emergência** | [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md#fluxo-7) |
| **Pagamento** | [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md#fluxo-11) e [COMPONENTES.md](./COMPONENTES.md#26-api-de-pagamento) |
| **API** | [COMPONENTES.md](./COMPONENTES.md#2-apis-do-backend) |
| **Modelo de Dados** | [COMPONENTES.md](./COMPONENTES.md#1-modelos-de-dados) |
| **Lock/Concorrência** | [ARQUITETURA.md](./ARQUITETURA.md#23-state-management--concurrency) |
| **Segurança** | [ARQUITETURA.md](./ARQUITETURA.md#6-considerações-de-segurança) |
| **LLM/Agent** | [ARQUITETURA.md](./ARQUITETURA.md#1-camada-de-interação-agent-layer) |
| **Saúde Mental** | [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md#81-saúde-mental-psicologiapsiquiatria) |

---

## ⏱️ Tempo de Leitura Estimado

| Documento | Tempo |
|-----------|-------|
| README.md | 10 min |
| ARQUITETURA.md | 45 min |
| FLUXOS_PRINCIPAIS.md | 60 min |
| REGRAS_NEGOCIO.md | 30 min |
| COMPONENTES.md | 40 min |
| GLOSSARIO.md | 20 min |
| **Total** | **3h 25min** |

---

## 📋 Checklist de Preparação Para Implementação

### Fase 1: Compreensão
- [ ] Leu README.md
- [ ] Entendeu visão geral
- [ ] Conhece os 12 fluxos principais
- [ ] Consultou GLOSSARIO.md para termos desconhecidos

### Fase 2: Design
- [ ] Revisou ARQUITETURA.md
- [ ] Entendeu padrões de design
- [ ] Documentou schema do BD
- [ ] Definiu APIs

### Fase 3: Desenvolvimento
- [ ] Implementou modelos de dados
- [ ] Implementou APIs (CRUD)
- [ ] Implementou sistema de lock
- [ ] Implementou validações
- [ ] Implementou integração LLM

### Fase 4: Teste
- [ ] Testou agendamento (happy path)
- [ ] Testou agendamento (edge cases)
- [ ] Testou cancelamento
- [ ] Testou desconto
- [ ] Testou pagamento

### Fase 5: Deploy
- [ ] Aplicou segurança (criptografia, rate limiting)
- [ ] Configurou monitoring
- [ ] Documentou deployment
- [ ] Treinou equipe

---

## 🤝 Contribuindo Com a Documentação

Se encontrar:
- ❌ **Erros ou inconsistências**: Abra uma issue
- 🤔 **Dúvidas ou falta de clareza**: Sugira melhorias
- ✨ **Novos casos de uso**: Adicione fluxos

Formato de sugestão:
```markdown
**Arquivo**: [nome do arquivo]
**Linha**: [número da linha, se aplicável]
**Problema**: [descreva]
**Sugestão**: [sua sugestão]
```

---

## 📞 Referências e Links Externos

### Tecnologias Mencionadas
- [OpenAI API](https://platform.openai.com/docs)
- [Anthropic Claude](https://claude.ai)
- [LangChain](https://python.langchain.com)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Redis](https://redis.io/documentation)
- [Stripe API](https://stripe.com/docs/api)
- [MercadoPago API](https://www.mercadopago.com.br/developers/pt)

### Padrões e Standards
- [REST API Best Practices](https://restfulapi.net/)
- [OWASP Security](https://owasp.org/)
- [GDPR/LGPD](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)

### Recursos de Saúde Mental (Brasil)
- **CVV** (Centro de Valorização da Vida): 188 (ligação gratuita)
- **SAMU**: 192
- **Polícia**: 190

---

**Documento atualizado em**: Junho 2026  
**Versão**: 1.0  
**Status**: ✅ Pronto para Implementação

---

**Voltar para**: [README.md](../README.md)

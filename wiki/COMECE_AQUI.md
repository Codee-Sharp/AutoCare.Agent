# 🚀 COMECE AQUI

Bem-vindo ao **AutoCare Agent**! Este é seu ponto de entrada na documentação.

---

## ❓ Quem é Você?

Escolha seu perfil para receber um roteiro personalizado:

### 👤 **[1] Sou um PACIENTE / USUÁRIO**
Quero entender como usar a aplicação.

**Tempo**: 15 minutos  
**Leia**:
1. [O que é AutoCare Agent?](#-o-que-é-autocare-agent)
2. [README.md - Visão Geral](../README.md)
3. [GLOSSARIO.md - Termos para Usuários](./GLOSSARIO.md#se-você-é-um-paciente--usuário-leigo)

**Principais aprendizados**:
- ✅ Como agendar um horário
- ✅ Como cancelar com segurança
- ✅ Quais descontos você pode ter
- ✅ Quem contactar em emergência

---

### 🏥 **[2] Sou GESTOR / STAKEHOLDER**
Quero entender a estratégia de negócio e ganhos.

**Tempo**: 45 minutos  
**Leia**:
1. [README.md - Completo](../README.md)
2. [FLUXOS_PRINCIPAIS.md - Visão Geral](./FLUXOS_PRINCIPAIS.md)
3. [REGRAS_NEGOCIO.md - Descontos e Cross-Selling](./REGRAS_NEGOCIO.md#3-regras-de-desconto)

**Principais aprendizados**:
- ✅ Como o agente aumenta agendamentos
- ✅ Estratégia de conversão e cross-selling
- ✅ Redução de no-shows
- ✅ Detecção de crises
- ✅ Integração com pagamento
- ✅ ROI esperado

---

### 👨‍💼 **[3] Sou RECEPCIONISTA / ATENDENTE**
Quero saber como o sistema me ajuda no dia a dia.

**Tempo**: 30 minutos  
**Leia**:
1. [FLUXOS_PRINCIPAIS.md - Fluxos 6, 7, 8](./FLUXOS_PRINCIPAIS.md)
2. [GLOSSARIO.md - Termos para Atendentes](./GLOSSARIO.md#se-você-é-um-recepcionista-atendente)

**Principais aprendizados**:
- ✅ Quais são meus alertas
- ✅ Como acessar o dossiê do chat
- ✅ Protocolo de crise
- ✅ Como confirmar pagamentos
- ✅ Dashboard de agendamentos

---

### 👨‍💻 **[4] Sou DESENVOLVEDOR BACKEND**
Quero implementar as APIs e lógica de negócio.

**Tempo**: 3+ horas  
**Leia em Ordem**:
1. [README.md](../README.md)
2. [ARQUITETURA.md](./ARQUITETURA.md) ⭐ IMPORTANTE
3. [COMPONENTES.md](./COMPONENTES.md) - APIs e Modelos
4. [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md) - Especialmente Agendamento
5. [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md) - Validações
6. [VISAO_GERAL.md](./VISAO_GERAL.md) - Diagramas

**Checklist de Implementação**:
```
FASE 1: Setup Infrastructure
  ☐ PostgreSQL + Redis + RabbitMQ

FASE 2: Database & Models
  ☐ Schema + Índices

FASE 3: Backend APIs
  ☐ CRUD endpoints
  ☐ Autenticação

FASE 4: Transações Críticas
  ☐ Lock Temporário (CRITICAL)
  ☐ Agendamento com ACID
  ☐ Cancelamento
  ☐ Pagamento

FASE 5: Integrações
  ☐ Payment Gateway
  ☐ Email/SMS
  ☐ Event Emitters

FASE 6: Segurança
  ☐ Criptografia
  ☐ Rate Limiting
  ☐ Auditoria
```

---

### 🤖 **[5] Sou ESPECIALISTA EM IA / AGENTE**
Quero implementar o LLM e orquestração.

**Tempo**: 2+ horas  
**Leia em Ordem**:
1. [README.md](../README.md)
2. [ARQUITETURA.md - Camada de Interação](./ARQUITETURA.md#1-camada-de-interação-agent-layer)
3. [COMPONENTES.md - Tools do Agent](./COMPONENTES.md#4-tools-do-agent)
4. [FLUXOS_PRINCIPAIS.md - Fluxo 1, 6, 7](./FLUXOS_PRINCIPAIS.md)
5. [VISAO_GERAL.md - Diagramas](./VISAO_GERAL.md)

**Checklist de Implementação**:
```
☐ Integração com LLM (OpenAI/Claude)
☐ System Prompt dinâmico
☐ Context Injection
☐ Tool Calling
☐ Intent Detection
☐ Crisis Detection
☐ Persona Routing
☐ Dossier Generation (para handoff)
☐ Safety Filters
```

---

### 🎨 **[6] Sou DESIGNER / DEVELOPER FRONTEND**
Quero criar a interface intuitiva.

**Tempo**: 1 hora  
**Leia em Ordem**:
1. [FLUXOS_PRINCIPAIS.md - Visão Geral](./FLUXOS_PRINCIPAIS.md)
2. [COMPONENTES.md - APIs do Backend](./COMPONENTES.md#2-apis-do-backend)
3. [VISAO_GERAL.md](./VISAO_GERAL.md)

**Checklist de Interface**:
```
☐ Calendário de disponibilidade
☐ Seleção de serviço
☐ Validação de dados
☐ Confirmação com lock visual
☐ Exibição de descontos
☐ Payment integration
☐ Dashboard de agendamentos
☐ Responsivo (mobile-first)
```

---

### 🔒 **[7] Sou ESPECIALISTA EM SEGURANÇA**
Quero garantir proteção de dados.

**Tempo**: 1+ horas  
**Leia em Ordem**:
1. [ARQUITETURA.md - Segurança](./ARQUITETURA.md#6-considerações-de-segurança)
2. [REGRAS_NEGOCIO.md - Regras de Segurança](./REGRAS_NEGOCIO.md#7-regras-de-segurança)
3. [COMPONENTES.md - Modelos de Dados](./COMPONENTES.md#1-modelos-de-dados)

**Checklist de Segurança**:
```
☐ Criptografia em repouso (AES-256)
☐ Criptografia em trânsito (TLS)
☐ Autenticação (OAuth 2.0 / JWT)
☐ Autorização (RBAC)
☐ Rate Limiting
☐ Detecção de anomalias
☐ Auditoria de acesso
☐ Sanitização de inputs
☐ GDPR/LGPD compliance
```

---

## 📚 O Que É AutoCare Agent?

É um **agente autônomo baseado em IA** que gerencia o atendimento, agendamento e experiência do paciente em clínicas de saúde, psicologia, estética e beleza.

### 🎯 Objetivos:
- ✅ Automatizar agendamentos 24/7
- ✅ Reduzir carga da recepção
- ✅ Aumentar conversão (descontos + cross-selling)
- ✅ Reduzir no-shows (lembretes automáticos)
- ✅ Proteger pacientes de saúde mental (detecção de crise)
- ✅ Integração com pagamento (sinal/integral)

### 🏢 Domínios:
- **Saúde Mental** (Psicologia, Psiquiatria) - Tom acolhedor
- **Estética** (Limpeza, Peeling, Botox, etc) - Tom entusiasta
- **Beleza** (Salão, Cabelo, Unhas) - Tom amigável
- Qualquer especialidade em clínicas

### 🔄 Os 12 Fluxos:
1. Acolhimento e Triagem
2. Base de Conhecimento (RAG)
3. Negociação e Descontos
4. **Agendamento** ⭐ (Core Business)
5. Self-Service (Gerenciamento de agendamentos)
6. Handoff Inteligente (Transferência para humano)
7. **Detecção de Crise** ⭐ (Protocolo de emergência)
8. Confirmação Ativa (Lembretes)
9. Fila de Espera (Waitlist)
10. Agendamento Múltiplo (Cross-Selling)
11. Cobrança (Integração com Payment Gateway)
12. Multimodalidade (Imagens, Documentos)

---

## 📖 Estrutura da Documentação

```
📚 DOCUMENTAÇÃO
│
├─ 📖 README.md                 ← Visão geral do projeto
│
├─ 📁 wiki/
│  ├─ COMECE_AQUI.md           ← Você está aqui!
│  ├─ INDEX.md                 ← Índice completo
│  ├─ VISAO_GERAL.md           ← Diagramas visuais
│  ├─ ARQUITETURA.md           ← Estrutura técnica
│  ├─ FLUXOS_PRINCIPAIS.md     ← 12 fluxos detalhados
│  ├─ REGRAS_NEGOCIO.md        ← Políticas e regras
│  ├─ COMPONENTES.md           ← APIs e modelos de dados
│  ├─ GLOSSARIO.md             ← Dicionário de termos
│  └─ README.md                ← Índice da wiki
│
└─ 📁 (código será aqui)
```

---

## ⏱️ Tempo de Leitura Por Perfil

| Perfil | Tempo | Arquivos |
|--------|-------|----------|
| Paciente | 15 min | README + GLOSSARIO |
| Gestor | 45 min | README + FLUXOS + REGRAS |
| Recepcionista | 30 min | FLUXOS (6,7,8) + GLOSSARIO |
| Dev Backend | 3+ h | ARQUITETURA + COMPONENTES + FLUXOS + REGRAS |
| Dev Frontend | 1 h | FLUXOS + COMPONENTES (APIs) |
| Especialista IA | 2+ h | ARQUITETURA (Agent) + COMPONENTES (Tools) |
| Especialista Segurança | 1+ h | ARQUITETURA (Seg.) + REGRAS (Seg.) |

---

## 🔍 Procura Por Algo Específico?

### 🎯 Funcionalidades
- **Agendamento**: [FLUXOS_PRINCIPAIS.md - Fluxo 4](./FLUXOS_PRINCIPAIS.md#fluxo-4-agendamento-rf09-12--critical)
- **Cancelamento**: [FLUXOS_PRINCIPAIS.md - Fluxo 5](./FLUXOS_PRINCIPAIS.md#fluxo-5-self-service-rf13-15)
- **Desconto**: [FLUXOS_PRINCIPAIS.md - Fluxo 3](./FLUXOS_PRINCIPAIS.md#fluxo-3-negociação-e-descontos-rf07-08)
- **Crise**: [FLUXOS_PRINCIPAIS.md - Fluxo 7](./FLUXOS_PRINCIPAIS.md#fluxo-7-detecção-de-crise-rf19-20--critical)

### 🛠️ Técnico
- **Arquitetura**: [ARQUITETURA.md](./ARQUITETURA.md)
- **APIs**: [COMPONENTES.md - APIs](./COMPONENTES.md#2-apis-do-backend)
- **Modelos de Dados**: [COMPONENTES.md - Modelos](./COMPONENTES.md#1-modelos-de-dados)
- **Lock de Concorrência**: [ARQUITETURA.md - State Management](./ARQUITETURA.md#23-state-management--concurrency)
- **Segurança**: [ARQUITETURA.md - Segurança](./ARQUITETURA.md#6-considerações-de-segurança)

### 📋 Negócio
- **Regras de Agendamento**: [REGRAS_NEGOCIO.md - Seção 1](./REGRAS_NEGOCIO.md#1-regras-de-agendamento)
- **Regras de Cancelamento**: [REGRAS_NEGOCIO.md - Seção 2](./REGRAS_NEGOCIO.md#2-regras-de-cancelamento)
- **Descontos**: [REGRAS_NEGOCIO.md - Seção 3](./REGRAS_NEGOCIO.md#3-regras-de-desconto)
- **Saúde Mental**: [REGRAS_NEGOCIO.md - Seção 8.1](./REGRAS_NEGOCIO.md#81-saúde-mental-psicologiapsiquiatria)

### 📖 Termos
- **Glossário Completo**: [GLOSSARIO.md](./GLOSSARIO.md)
- **Abreviações**: [GLOSSARIO.md - Abreviações](./GLOSSARIO.md#abreviações)
- **FAQ**: [GLOSSARIO.md - Dúvidas Frequentes](./GLOSSARIO.md#dúvidas-frequentes)

---

## 🎓 Roteiros de Aprendizado

### **Para Técnico Completo** (10 horas)
```
Dia 1:
  ├─ README.md (20 min)
  ├─ VISAO_GERAL.md (30 min)
  └─ ARQUITETURA.md (1h 45min)

Dia 2:
  ├─ COMPONENTES.md - Modelos (45 min)
  ├─ COMPONENTES.md - APIs (45 min)
  └─ COMPONENTES.md - Tools (30 min)

Dia 3:
  ├─ FLUXOS_PRINCIPAIS.md (2h)
  └─ REGRAS_NEGOCIO.md (1h)

Dia 4+: Implementação
  └─ Retornar aos arquivos conforme necessário
```

### **Para Leitura Rápida** (1 hora)
```
├─ README.md (20 min)
├─ VISAO_GERAL.md (20 min)
├─ INDEX.md (10 min)
└─ GLOSSARIO.md (10 min)
```

### **Para Implementar Agora** (consultar conforme necessário)
```
Agendamento?
  └─ ARQUITETURA.md (Fluxo end-to-end) + COMPONENTES.md (APIs)

Segurança?
  └─ ARQUITETURA.md (Considerações) + REGRAS_NEGOCIO.md (Seg.)

Validações?
  └─ REGRAS_NEGOCIO.md

LLM Integration?
  └─ ARQUITETURA.md (Agent Layer) + COMPONENTES.md (Tools)
```

---

## ✅ Antes de Começar

Certifique-se que você:
- ✅ Tem permissão para acessar esta documentação
- ✅ Entende o contexto do projeto (saúde/beleza/estética)
- ✅ Tem interesse genuíno em aprender
- ✅ Pode dedicar tempo para leitura/implementação

---

## 🆘 Dúvidas?

1. **Procure no [GLOSSARIO.md](./GLOSSARIO.md)** para termos desconhecidos
2. **Consulte o [INDEX.md](./INDEX.md)** para navegação completa
3. **Veja o [VISAO_GERAL.md](./VISAO_GERAL.md)** para diagramas visuais
4. **Verifique [FAQ](./GLOSSARIO.md#dúvidas-frequentes)** para perguntas comuns

---

## 🚀 Pronto?

Escolha seu perfil acima e comece a leitura recomendada!

### **Atalhos Rápidos**:
- 👤 [Paciente](#-sou-um-paciente--usuário)
- 🏥 [Gestor](#-sou-gestor--stakeholder)
- 👨‍💼 [Recepcionista](#-sou-recepcionista--atendente)
- 👨‍💻 [Dev Backend](#-sou-desenvolvedor-backend)
- 🎨 [Dev Frontend](#-sou-designer--developer-frontend)
- 🤖 [Especialista IA](#-sou-especialista-em-ia--agente)
- 🔒 [Especialista Segurança](#-sou-especialista-em-segurança)

---

**Boa leitura! 📚**

Última atualização: Junho 2026  
Status: ✅ Pronto Para Implementação

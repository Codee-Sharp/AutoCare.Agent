# 📚 Wiki - AutoCare Agent

Documentação completa e estruturada do projeto **AutoCare Agent**.

## 📖 Arquivos da Documentação

```
wiki/
├── INDEX.md                 # 📑 Índice e guia de leitura (COMECE AQUI!)├── STACK_REAL.md           # 🔧 Stack tecnológico + integração (ARQUITETURA REAL)├── ARQUITETURA.md          # 🏗️  Estrutura técnica e padrões
├── FLUXOS_PRINCIPAIS.md    # 📊 Detalhamento de todos os 12 fluxos
├── REGRAS_NEGOCIO.md       # 📋 Regras parametrizadas e políticas
├── COMPONENTES.md          # 🔧 APIs, modelos de dados e interfaces
└── GLOSSARIO.md            # 📖 Dicionário de termos
```

---

## 🎯 Comece Por Aqui

### 0️⃣ **Stack Tecnológico Real** (15 min) 🌟 **IMPORTANTE**
→ Leia: [STACK_REAL.md](./STACK_REAL.md) - Entenda que o Agent fica ATRÃS de uma aplicação interna

### 1️⃣ **Entender o Projeto** (10 min)
→ Leia: [INDEX.md](./INDEX.md#-comece-por-aqui)

### 2️⃣ **Aprender a Arquitetura** (45 min)
→ Leia: [ARQUITETURA.md](./ARQUITETURA.md)

### 3️⃣ **Ver os Fluxos Funcionais** (60 min)
→ Leia: [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md)

### 4️⃣ **Conhecer as Regras** (30 min)
→ Leia: [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md)

### 5️⃣ **Implementar as APIs** (40 min)
→ Leia: [COMPONENTES.md](./COMPONENTES.md)

### 6️⃣ **Esclarecer Termos** (20 min)
→ Leia: [GLOSSARIO.md](./GLOSSARIO.md)

---

## 👥 Guia Por Perfil

| Você é | Leia | Tempo |
|--------|------|-------|
| **Paciente/Leigo** | INDEX.md → README → Glossário | 15 min |
| **Gestor/Stakeholder** | README → FLUXOS → REGRAS | 45 min |
| **Recepcionista** | FLUXOS (6,7,8) → Glossário | 30 min |
| **Dev Backend** | ARQUITETURA → COMPONENTES → REGRAS | 3h |
| **Dev Frontend** | FLUXOS → COMPONENTES (APIs) | 1h |
| **Especialista IA** | ARQUITETURA → COMPONENTES (Tools) | 2h |
| **Especialista Segurança** | ARQUITETURA (Seg.) → REGRAS (Seg.) | 1h |

---

## 📊 Estrutura do Projeto

```
AutoCare.Agent/
├── README.md              # Visão geral do projeto
├── wiki/
│   ├── INDEX.md          # 🚀 Você está aqui!
│   ├── ARQUITETURA.md    # Estrutura técnica
│   ├── FLUXOS_PRINCIPAIS.md   # 12 fluxos detalhados
│   ├── REGRAS_NEGOCIO.md      # Políticas e regras
│   ├── COMPONENTES.md    # APIs e modelos
│   └── GLOSSARIO.md      # Dicionário de termos
└── ... (código será aqui)
```

---

## 🔄 Os 12 Fluxos Principais

1. ✅ **Acolhimento e Triagem** - Identificar e contextualizar paciente
2. ✅ **Base de Conhecimento** - RAG para consultar serviços
3. ✅ **Negociação e Descontos** - Oferecer promoções controladas
4. ⭐ **Agendamento** - Core business (crítico!)
5. ✅ **Self-Service** - Paciente gerencia seus agendamentos
6. ✅ **Handoff Inteligente** - Transferir para atendente humano
7. ⭐ **Detecção de Crise** - Protocolo de emergência
8. ✅ **Confirmação Ativa** - Lembretes proativos
9. ✅ **Fila de Espera** - Waitlist para slots indisponíveis
10. ✅ **Agendamento Múltiplo** - Cross-selling inteligente
11. ✅ **Cobrança** - Integração com payment gateway
12. ✅ **Multimodalidade** - Suporte a imagens e documentos

→ Detalhes: [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md)

---

## 🔍 Procura Por Algo Específico?

| Assunto | Arquivo | Seção |
|---------|---------|-------|
| Como implementar agendamento | ARQUITETURA | 4. Fluxo End-to-End |
| Regras de cancelamento | REGRAS_NEGOCIO | 2. Cancelamento |
| Descontos e promoções | REGRAS_NEGOCIO | 3. Desconto |
| Estrutura do banco de dados | COMPONENTES | 1. Modelos de Dados |
| Endpoints da API | COMPONENTES | 2. APIs do Backend |
| Tools do LLM | COMPONENTES | 4. Tools do Agent |
| Segurança e criptografia | ARQUITETURA | 6. Segurança |
| Detecção de crise | FLUXOS_PRINCIPAIS | Fluxo 7 |
| Termos técnicos | GLOSSARIO | Termos Técnicos |
| Abreviações | GLOSSARIO | Abreviações |

---

## ✨ Características Principais

### 🤖 Inteligência Artificial
- LLM com contexto injetado dinamicamente
- Tool Calling para ações estruturadas
- Detecção de intenções e crises
- Deflexão suave e handoff inteligente

### 🔐 Segurança
- Criptografia em repouso e trânsito
- Rate limiting e proteção DDoS
- Auditoria de acesso
- Máxima privacidade para saúde mental

### 💼 Negócio
- Motor de descontos parametrizado
- Cross-selling inteligente
- Fila de espera automática
- Integração com pagamento

### 🏥 Saúde Mental
- Protocolo especial para emergências
- Cancelamento sem taxa
- Triagem automática de risco
- Contatos de emergência

---

## 📚 Tempo de Leitura Total

| Documento | Tempo |
|-----------|-------|
| INDEX.md | 10 min |
| ARQUITETURA.md | 45 min |
| FLUXOS_PRINCIPAIS.md | 60 min |
| REGRAS_NEGOCIO.md | 30 min |
| COMPONENTES.md | 40 min |
| GLOSSARIO.md | 20 min |
| **Total** | **3h 25min** |

---

## 📞 Estrutura Recomendada Para Estudar

### Dia 1: Fundamentos (1 hora)
- [ ] INDEX.md (10 min)
- [ ] README.md (20 min)
- [ ] GLOSSARIO.md (30 min)

### Dia 2: Visão Técnica (1.5 horas)
- [ ] ARQUITETURA.md (45 min)
- [ ] COMPONENTES.md - Modelos (45 min)

### Dia 3: Fluxos e Regras (2 horas)
- [ ] FLUXOS_PRINCIPAIS.md (60 min)
- [ ] REGRAS_NEGOCIO.md (30 min)
- [ ] COMPONENTES.md - APIs (30 min)

### Dia 4: Implementação
- [ ] Revisar ARQUITETURA.md
- [ ] Revisar COMPONENTES.md
- [ ] Começar codificação

---

## 🚀 Próximos Passos

1. **Leia** o INDEX.md para entender a estrutura
2. **Consulte** o arquivo relevante para seu papel
3. **Use** o GLOSSARIO.md para termos desconhecidos
4. **Implemente** baseado em ARQUITETURA e COMPONENTES
5. **Valide** usando FLUXOS_PRINCIPAIS e REGRAS_NEGOCIO

---

## 📝 Versão e Status

- **Versão**: 1.0
- **Data**: Junho 2026
- **Status**: ✅ Pronto Para Implementação
- **Última Atualização**: 2026-06-13

---

## 🤝 Contribuir

Se encontrar erros, omissões ou sugestões de melhoria, abra um issue ou pull request no repositório.

---

**[Voltar para README principal](../README.md)**

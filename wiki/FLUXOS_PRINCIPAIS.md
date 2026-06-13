# 📊 FLUXOS PRINCIPAIS DO SISTEMA

## Índice Rápido

| # | Fluxo | RF | Status |
|---|-------|-----|--------|
| 1 | Acolhimento e Triagem | RF01-03 | Core |
| 2 | Base de Conhecimento (RAG) | RF04-06 | Core |
| 3 | Negociação e Descontos | RF07-08 | Core |
| 4 | Agendamento | RF09-12 | **Critical** |
| 5 | Self-Service | RF13-15 | Core |
| 6 | Handoff Inteligente | RF16-18 | Core |
| 7 | Detecção de Crise | RF19-20 | **Critical** |
| 8 | Confirmação Ativa | RF21-23 | Core |
| 9 | Fila de Espera | RF24-25 | Opcional |
| 10 | Cross-Selling | RF26-27 | Opcional |
| 11 | Cobrança | RF28-29 | Core |
| 12 | Multimodalidade | RF31-32 | Opcional |

---

## FLUXO 1️⃣: Acolhimento e Triagem (RF01-03)

### 🎯 Objetivo
Identificar o paciente, recuperar seu contexto e adaptar o comportamento do agente.

### 📝 Requisitos Funcionais
- **RF01**: Identificação de Usuário
- **RF02**: Injeção Dinâmica de Contexto
- **RF03**: Roteamento de Persona

### 🔄 Sequência Detalhada

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as Agent
    participant DB as Banco de Dados
    
    P->>A: Envia mensagem inicial
    Note over A: [1] Extrair identificador<br/>(phone, email, user_id)
    
    A->>DB: Consultar paciente_id
    activate DB
    alt Paciente Encontrado
        DB-->>A: Retorna perfil completo
        Note over A: [2] Injetar dados no System Prompt:<br/>- Nome<br/>- Histórico recente<br/>- Preferências<br/>- Especialidade
    else Novo Paciente
        DB-->>A: Null
        Note over A: [2] Injetar novo perfil<br/>com saudação genérica
    end
    deactivate DB
    
    Note over A: [3] Selecionar Persona:<br/>IF especialidade IN ('psico', 'psiq')<br/>  → Tom clínico/acolhedor<br/>ELSE<br/>  → Tom comercial/entusiástico
    
    A->>P: Resposta personalizada
    Note over P: "Olá João! Bem-vindo de volta 👋<br/>Como posso ajudá-lo hoje?"
```

### 💾 Dados Injetados no System Prompt

```json
{
  "sistema": {
    "data_atual": "2026-06-13",
    "especialidade": "estética",
    "persona": "comercial_entusiasta"
  },
  "paciente": {
    "id": "uuid-123",
    "nome": "João",
    "primeira_visita": false,
    "ultimo_agendamento": "2026-05-15",
    "ultimo_servico": "Limpeza de Pele",
    "historico_recente": [
      {
        "data": "2026-05-15",
        "servico": "Limpeza de Pele",
        "profissional": "Maria (Esteticista)",
        "comentario_paciente": "Amei! Voltei com a pele brilhando 😍"
      }
    ],
    "servicos_preferidos": ["Limpeza de Pele", "Hidratação"],
    "frequencia_estimada": "30 dias"
  },
  "restricoes": {
    "apenas_servicos_catalogados": true,
    "nunca_inventar_precos": true,
    "redirecionamento_medico_complexo": true
  }
}
```

### ✅ Critérios de Sucesso
- ✅ Paciente se sente reconhecido
- ✅ Tone of voice correto para especialidade
- ✅ Contexto do histórico está injetado

---

## FLUXO 2️⃣: Base de Conhecimento (RAG) (RF04-06)

### 🎯 Objetivo
Fornecer informações precisas sobre serviços, procedimentos, preços e benefícios.

### 📝 Requisitos Funcionais
- **RF04**: Consulta de Catálogo (RAG/API)
- **RF05**: Recuperação Dinâmica de Preços
- **RF06**: Limite de Escopo (Safety Filter)

### 🔄 Sequência

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as Agent (LLM)
    participant API as Service API
    participant DB as Banco de Dados
    
    P->>A: "Qual é o preço da limpeza de pele?"
    
    Note over A: [1] Detectar intenção:<br/>CONSULTA_SERVICO
    
    A->>A: [2] Validar escopo:<br/>✓ "Limpeza de pele" está no catálogo?
    
    alt Serviço não existe no catálogo
        A-->>P: "Desculpe, não tenho informação<br/>sobre esse serviço. Posso ajudá-lo<br/>com nossos serviços disponíveis?"
    else Serviço existe
        A->>API: buscar_detalhes_servico(nome)
        activate API
        API->>DB: SELECT * FROM Servicos WHERE nome LIKE ?
        activate DB
        DB-->>API: Retorna registro
        deactivate DB
        
        API-->>A: {<br/>  "id": "uuid-xyz",<br/>  "nome": "Limpeza de Pele",<br/>  "preco": 150.00,<br/>  "duracao": 60,<br/>  "beneficios": [...],<br/>  "orientacoes": [...]<br/>}
        deactivate API
        
        Note over A: [3] Preparar resposta<br/>(NUNCA alterar preço)
        
        A-->>P: "A Limpeza de Pele custa R$ 150,00<br/>e leva 1 hora. Benefícios:<br/>- Remove impurezas<br/>- Melhora textura...<br/>Quer agendar?"
    end
```

### 🛡️ Safety Filters

| Filter | Ação |
|--------|------|
| **Serviço não existe** | Sugerir alternativas do catálogo |
| **Paciente pede preço "normal"** | Retornar SEMPRE da API/BD |
| **Consulta médica complexa** | "Você deve consultar o médico" |
| **Pergunta sobre diagnóstico** | Redirecionar para profissional |

### 💾 Estrutura do Serviço (Catálogo)

```json
{
  "id": "uuid-estética-001",
  "nome": "Limpeza de Pele",
  "descricao": "Procedimento de higienização profunda da pele",
  "categoria": "estética",
  "duracao_minutos": 60,
  "preco_base": 150.00,
  "beneficios": [
    "Remove impurezas",
    "Melhora textura",
    "Prepara para outros procedimentos"
  ],
  "orientacoes": {
    "pre": "Nenhuma preparação necessária",
    "pos": "Evitar sol por 48h"
  },
  "contraindicacoes": [
    "Pele muito sensível inflamada"
  ],
  "profissionais_habilitados": ["uuid-maria", "uuid-ana"],
  "ativo": true
}
```

---

## FLUXO 3️⃣: Negociação e Descontos (RF07-08)

### 🎯 Objetivo
Ofertar descontos de forma controlada e estratégica.

### 📝 Requisitos Funcionais
- **RF07**: Validação de Elegibilidade
- **RF08**: Condicionalidade de Conversão

### 🔄 Sequência

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as Agent
    participant API as Desconto API
    participant DB as Banco de Dados
    
    P->>A: "Tem algum desconto?"
    
    Note over A: [1] Extrair contexto:<br/>- paciente_id<br/>- servico_id (se mencionado)<br/>- motivo (primeira visita, lealdade, etc)
    
    A->>API: validar_desconto({<br/>  paciente_id,<br/>  servico_id,<br/>  motivo<br/>})
    
    activate API
    API->>DB: Consultar regras parametrizadas
    activate DB
    DB-->>API: Retorna regras ativas
    deactivate DB
    
    Note over API: [2] Aplicar regras:<br/>- Primeira visita? → 15%<br/>- Lealdade (3+ serviços)? → 10%<br/>- Horário baixa demanda? → 5%<br/>- Política máximo? → Capped
    
    alt Elegível
        API-->>A: {<br/>  "elegivel": true,<br/>  "desconto_percentual": 15,<br/>  "condicoes": {<br/>    "descricao": "Primeira visita",<br/>    "validade": "2026-06-30",<br/>    "requer_agendamento_imediato": true<br/>  }<br/>}
    else Inelegível
        API-->>A: {<br/>  "elegivel": false,<br/>  "motivo": "Já realizou 5 descontos<br/>este mês"<br/>}
    end
    deactivate API
    
    alt Elegível
        A-->>P: "Ótima notícia! 🎉<br/>Como primeira visita, você ganha 15% OFF!<br/>Limpeza de Pele: de R$ 150 → R$ 127,50<br/><br/>Quer agendar agora?"
        
        Note over A: [3] Condicionar desconto:<br/>Oferta válida APENAS se<br/>agendamento confirmado HOJE
        
    else Inelegível
        A-->>P: "Infelizmente você já usou<br/>seus descontos mensais.<br/>Mas temos ótimas promoções<br/>em novembro!"
    end
```

### 📋 Regras de Desconto (Parametrizadas)

```json
{
  "regras_desconto": [
    {
      "id": "primeira_visita",
      "nome": "Primeira Visita",
      "condicoes": {
        "primeira_visita": true,
        "especialidades": ["estética", "salão"]
      },
      "desconto_percentual": 15,
      "desconto_fixo": null,
      "validade_dias": 30,
      "usos_por_paciente": 1,
      "requer_agendamento_imediato": true
    },
    {
      "id": "lealdade_3_servicos",
      "nome": "Lealdade (3+ Serviços)",
      "condicoes": {
        "total_servicos_realizados": { "gte": 3 },
        "dias_desde_ultimo": { "gte": 30 }
      },
      "desconto_percentual": 10,
      "usos_por_paciente": null,
      "requer_agendamento_imediato": false
    },
    {
      "id": "horario_baixa_demanda",
      "nome": "Horário de Baixa Demanda",
      "condicoes": {
        "hora_inicio": { "gte": "10:00", "lte": "12:00" },
        "dia_semana": ["terça", "quarta"],
        "ocupacao_agenda": { "lte": 30 }
      },
      "desconto_percentual": 5,
      "validade_minutos": 10
    }
  ],
  "politicas": {
    "desconto_maximo_acumulado": 25,
    "limite_descontos_mes": 5
  }
}
```

---

## FLUXO 4️⃣: Agendamento (RF09-12) ⭐ **CRITICAL**

### 🎯 Objetivo
Core business: Reservar horários com garantia de não double-booking.

### 📝 Requisitos Funcionais
- **RF09**: Consulta Parametrizada de Horários
- **RF10**: Sistema de Lock (Bloqueio Temporário)
- **RF11**: Validação e Coleta de Dados
- **RF12**: Efetivação Transacional

### 🔄 Sequência Completa

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as Agent
    participant SCHED as Scheduler API
    participant DB as Banco de Dados
    participant QUEUE as Message Queue
    
    P->>A: "Quero agendar limpeza de pele"
    
    A->>A: [1] Coletar parâmetros:<br/>- servico_id ✓<br/>- data_preferida?<br/>- profissional_preferido?
    
    Note over A: [2] Chamar Tool:<br/>buscar_disponibilidade(params)
    
    A->>SCHED: buscar_disponibilidade({<br/>  servico_id,<br/>  data_inicio: now,<br/>  data_fim: now + 30d,<br/>  profissional_id: null<br/>})
    
    activate SCHED
    SCHED->>DB: SELECT slots_livres<br/>WHERE agendamento_data BETWEEN<br/>AND NOT EXISTS (locks)<br/>LIMIT 10
    activate DB
    DB-->>SCHED: [3 horários]
    deactivate DB
    deactivate SCHED
    
    A-->>P: "Encontrei 3 opções:<br/>1) Seg 14:00 - Maria<br/>2) Ter 09:00 - Ana<br/>3) Qua 16:00 - Maria"
    
    P->>A: "Quero Seg 14:00"
    
    A->>A: [3] Validar dados obrigatórios<br/>IF cpf NOT IN db:<br/>  → Solicitar CPF<br/>IF email NOT IN db:<br/>  → Solicitar email
    
    Note over A: [4] Dados validados ✓
    
    A->>SCHED: confirmar_agendamento({<br/>  paciente_id: uuid-123,<br/>  servico_id: uuid-xyz,<br/>  profissional_id: uuid-maria,<br/>  data_hora: "2026-06-16 14:00",<br/>  cpf: "123.456.789-00",<br/>  email: "joao@email.com"<br/>})
    
    activate SCHED
    
    Note over SCHED: [TRANSAÇÃO DB INICIADA]
    
    SCHED->>DB: [1] Validar lock ainda ativo
    activate DB
    alt Lock expirou
        DB-->>SCHED: NULL
        SCHED-->>A: ❌ Erro: Horário não está mais<br/>reservado. Busque novos horários.
        Note over A: Voltar ao passo [2]
    else Lock válido
        DB-->>SCHED: Lock encontrado
    end
    
    SCHED->>DB: [2] INSERT Agendamento
    DB-->>SCHED: ✓ Agendamento criado<br/>protocolo: AG-20260616-001
    
    SCHED->>DB: [3] DELETE Lock Temporário
    DB-->>SCHED: ✓ Lock removido
    
    SCHED->>DB: [4] INSERT Lembretes (24h, 48h)
    DB-->>SCHED: ✓ Lembretes criados
    
    Note over SCHED: [TRANSAÇÃO DB FINALIZADA] ✓
    deactivate DB
    
    SCHED-->>A: {<br/>  "status": "confirmado",<br/>  "protocolo": "AG-20260616-001",<br/>  "agendamento": {...}<br/>}
    
    deactivate SCHED
    
    Note over A: [5] Disparar eventos
    
    A->>QUEUE: PublicarEvento:<br/>agendamento.confirmado
    activate QUEUE
    QUEUE->>QUEUE: Listeners:<br/>- EmailService<br/>- SMSService<br/>- HistoricoService<br/>- NotificacaoService
    deactivate QUEUE
    
    A-->>P: "✅ CONFIRMADO!<br/>Protocolo: AG-20260616-001<br/>📅 Seg, 16 de junho - 14:00<br/>🧑‍⚕️ Profissional: Maria<br/>💰 R$ 150,00<br/><br/>Orientações:<br/>- Chegar 10min antes<br/>- Evitar sol após procedimento<br/><br/>Receberá confirmação por email/SMS"
```

### 🔐 Lock Temporário

```json
{
  "id": "lock-temp-001",
  "agendamento_id": null,
  "paciente_id": "uuid-123",
  "profissional_id": "uuid-maria",
  "data_hora": "2026-06-16 14:00:00",
  "servico_id": "uuid-estética-001",
  "criado_em": "2026-06-13 15:30:00",
  "expira_em": "2026-06-13 15:35:00",
  "ttl_segundos": 300
}
```

### ✅ Validações Antes de Commit

| Validação | Erro |
|-----------|------|
| Lock ainda válido | "Horário não está mais disponível" |
| Dados obrigatórios completos | "Faltam dados (CPF, email)" |
| Paciente não tem 3+ agendamentos naquele dia | "Limite de agendamentos excedido" |
| Serviço não tem contraindicações | "Você não pode fazer este serviço" |

---

## FLUXO 5️⃣: Self-Service (RF13-15)

### 🎯 Objetivo
Permitir que pacientes gerenciem seus próprios agendamentos.

### 📝 Requisitos Funcionais
- **RF13**: Resumo de Agendamentos
- **RF14**: Liberação de Slot
- **RF15**: Validação de Regra de Cancelamento

### 🔄 Resumo de Agendamentos

```
PACIENTE: "Quais são meus agendamentos?"
    ↓
AGENT: Consulta BD → Lista futuros + histórico recente
    ↓
Próximos:
  1) Seg 16/jun - 14:00 | Limpeza de Pele (Maria) | R$ 150 | [CANCELAR]
  2) Seg 23/jun - 10:00 | Hidratação (Ana) | R$ 120 | [CANCELAR]

Histórico:
  ✓ Dom 15/jun - Limpeza de Pele (Maria) | Realizado
  ✓ Dom 08/jun - Hidratação (Ana) | Realizado
```

### 🔄 Cancelamento

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as Agent
    participant API as Cancelamento API
    participant DB as Banco de Dados
    
    P->>A: "Quero cancelar meu agendamento de Seg"
    
    A->>API: validar_cancelamento({<br/>  agendamento_id: "AG-20260616-001",<br/>  paciente_id: "uuid-123"<br/>})
    
    activate API
    API->>DB: SELECT agendamento WHERE id=?
    activate DB
    DB-->>API: Retorna agendamento
    deactivate DB
    
    Note over API: [1] Validar antecedência:<br/>Minimo: 24 horas antes
    
    alt Dentro do prazo
        API-->>A: {<br/>  "pode_cancelar": true,<br/>  "taxa": 0,<br/>  "motivo": "Cancelamento com<br/>antecedência mínima"<br/>}
    else Sem antecedência
        API-->>A: {<br/>  "pode_cancelar": true,<br/>  "taxa": 50,<br/>  "motivo": "Cancelamento com menos<br/>de 24h: taxa de 50%"<br/>}
    end
    deactivate API
    
    alt Saúde Mental (psicologia)
        A-->>P: "Entendi. Cancelar sem taxa ✓<br/>Vai estar tudo bem? Estou aqui<br/>se precisar conversar 💙"
    else Estética
        A-->>P: "Sem problemas! Você será<br/>reembolsado em até 2 dias úteis ✓"
    end
    
    P->>A: "Sim, cancela"
    
    A->>API: executar_cancelamento({<br/>  agendamento_id<br/>})
    
    activate API
    API->>DB: [TRANSAÇÃO]<br/>1. UPDATE agendamento status=cancelled<br/>2. DELETE locks<br/>3. INSERT nota histórico<br/>4. Processar reembolso
    activate DB
    DB-->>API: ✓
    deactivate DB
    deactivate API
    
    A-->>P: "✅ Cancelado com sucesso<br/>Protocolo: CAN-20260613-001<br/>Você será reembolsado em até 2 dias"
```

---

## FLUXO 6️⃣: Handoff Inteligente (RF16-18)

### 🎯 Objetivo
Transição suave para atendimento humano quando necessário.

### 📝 Requisitos Funcionais
- **RF16**: Deflexão Suave
- **RF17**: Fallback (Beco sem Saída)
- **RF18**: Geração de Dossiê

### 🔄 Sequência

```
PACIENTE: "Quero falar com um atendente"
    ↓
[1] Tentativa de Deflexão Suave:
    "Claro! Antes, posso te ajudar com
     algo específico? Por exemplo:
     - Agendar um horário?
     - Cancelar alguma coisa?
     - Dúvida sobre preços?"
    
    P: "Não, só quero falar com atendente"
    
[2] Validar Motivo:
    - Solicitação explícita? ✓ SIM
    - Ou ciclo infinito (5+ iterações)? ❌ NÃO
    → Proceder ao Handoff

[3] Gerar Dossiê:
    {
      "protocolo_chat": "CHAT-20260613-001",
      "paciente_id": "uuid-123",
      "paciente_nome": "João",
      "email": "joao@email.com",
      "telefone": "+5511999999999",
      "historico_conversa": [
        { "timestamp": "...", "autor": "paciente", "texto": "..." },
        { "timestamp": "...", "autor": "agent", "texto": "..." }
      ],
      "resumo_inteligente": {
        "intencao_principal": "Agendamento de limpeza de pele",
        "status_conversacao": "Agendamento pendente de confirmação",
        "dados_coletados": {
          "servico": "Limpeza de Pele",
          "profissional_preferido": "Maria",
          "data_preferida": "2026-06-16 14:00"
        },
        "proximos_passos": [
          "Coletar CPF",
          "Confirmar email",
          "Processar pagamento (desconto 15% aplicável)"
        ],
        "sentimento_paciente": "Positivo, engajado"
      }
    }

[4] Notificar Recepção:
    Dashboard da Recepção:
    
    🔔 NOVO CHAT PARA ATENDER
    ├─ Paciente: João (UUID-123)
    ├─ Telefone: +5511999999999
    ├─ Intenção: Agendamento
    ├─ Status: Parcialmente resolvido
    └─ [VER DOSSIÊ COMPLETO]

[5] Transferir para Atendente:
    A-->>P: "Vou conectar você com nossa
             recepção. Um momento..."
    
    P: Conectado com Atendente Humano ✓
```

---

## FLUXO 7️⃣: Detecção de Crise (RF19-20) ⭐ **CRITICAL**

### 🎯 Objetivo
Interceptar urgências médicas/psicológicas e ativar protocolo de emergência.

### 📝 Requisitos Funcionais
- **RF19**: Interceptação de Risco
- **RF20**: Protocolo de Emergência

### 🔄 Sequência

```mermaid
sequenceDiagram
    participant P as Paciente
    participant A as Agent
    participant SAFETY as Safety Module
    participant ALERT as Alert Service
    participant STAFF as Equipe Clínica
    
    P->>A: "Estou tendo pensamentos suicidas"
    
    A->>SAFETY: analisar_risco({<br/>  texto: "...",<br/>  especialidade: "psicologia",<br/>  paciente_id: "uuid-123"<br/>})
    
    activate SAFETY
    Note over SAFETY: [1] Classificação de Risco:<br/>├─ Keyword matching:<br/>│  ✓ "suicida" → CRÍTICO<br/>├─ Sentiment: NEGATIVO/ANGÚSTIA<br/>├─ Contexto: Saúde Mental<br/>└─ Score: 0.98 (ALTO RISCO)
    
    alt RISCO CRÍTICO DETECTADO
        SAFETY-->>A: {<br/>  "risco": "CRÍTICO",<br/>  "tipo": "suicidio",<br/>  "score": 0.98,<br/>  "protocolo": "ATIVAR_EMERGENCIA"<br/>}
        
        Note over A: [2] INTERRUPÇÃO IMEDIATA
        
        A->>A: [PARAR fluxo de agendamento]
        
        A-->>P: "🚨 Entendo que você está<br/>passando por um momento difícil.<br/>Você NÃO está sozinho.<br/><br/>CONTATOS DE EMERGÊNCIA:<br/>🆘 CVV: 188 (ligue ou chat)<br/>🚑 SAMU: 192<br/>🏥 Pronto-Socorro mais próximo"
        
        A->>ALERT: disparar_alerta({<br/>  tipo: "CRISE_SUICIDIO",<br/>  paciente_id: "uuid-123",<br/>  paciente_nome: "João",<br/>  timestamp: now,<br/>  texto_original: "...",<br/>  requer_acao_imediata: true<br/>})
        
        activate ALERT
        ALERT-->>STAFF: Webhook/Email/SMS/Push<br/>⚠️ ALERTA DE CRISE<br/>Paciente: João (123)<br/>Tipo: Ideação Suicida<br/>→ [ABRIR CHAMADO]
        deactivate ALERT
        
        A-->>P: "Estou conectando você com<br/>um profissional de nossa equipe<br/>que pode ajudar agora mesmo..."
        
        Note over STAFF: Profissional de saúde mental<br/>toma atendimento imediatamente
        
    else RISCO MODERADO
        SAFETY-->>A: {<br/>  "risco": "MODERADO",<br/>  "protocolo": "DEFLEXAO_SUAVE"<br/>}
        A-->>P: "Entendo suas preocupações.<br/>Recomendo agendar uma<br/>consulta com um profissional<br/>que pode ajudar melhor. Quer<br/>agendar agora?"
        
    else SEM RISCO
        A->>A: Continuar fluxo normal
    end
```

### 🚨 Gatilhos de Crise

| Gatilho | Tipo | Ação |
|---------|------|------|
| "suicida", "matar" | CRÍTICO | Emergência |
| "automutilação", "cortar" | CRÍTICO | Emergência |
| "desespero", "não aguento" | MODERADO | Escalação |
| Agressividade/abuso | CRÍTICO | Bloqueio + Alerta |
| Menção de arma/veneno | CRÍTICO | Emergência |

### 📞 Contatos de Emergência (Brasil)

```json
{
  "emergencia": {
    "samu": "192",
    "policia": "190",
    "corpo_de_bombeiros": "193"
  },
  "saude_mental": {
    "cvv_call": "188 (ligação gratuita)",
    "cvv_chat": "https://www.cvv.org.br/",
    "caps_servico_aberto": "24h em grandes cidades"
  }
}
```

---

## FLUXO 8️⃣: Confirmação Ativa (RF21-23)

### 🎯 Objetivo
Lembretes proativos para aumentar presença e reduzir no-shows.

### 📝 Requisitos Funcionais
- **RF21**: Disparo Proativo
- **RF22**: Interpretação de Intenção Ambígua
- **RF23**: Lembretes de Cuidados Prévios

### 🔄 Sequência (Worker/Cronjob)

```
[SCHEDULE: 48 horas antes de cada agendamento]

SELECT agendamentos WHERE
  data_hora = now() + 48h
  AND status = 'confirmado'
  AND lembrete_48h NOT SENT

FOR EACH agendamento:
  
  [1] Construir mensagem personalizada:
      "Olá João! 👋
       Lembrete: Seu agendamento de
       Limpeza de Pele está marcado para
       
       📅 Seg, 16 de junho às 14:00
       📍 Nossa clínica
       👩‍⚕️ Com Maria
       
       Orientações:
       ✓ Chegue 10 minutos antes
       ✓ Evite maquiagem
       ✓ Após: evitar sol por 48h
       
       Confirmar: Sim / Não / Reagendar?"
  
  [2] Enviar via SMS/WhatsApp/Email
  
  [3] Aguardar resposta do paciente
      (timeout: 48 horas)

[SCHEDULE: 24 horas antes]
  Repetir processo com mensagem diferente

[RESPONSE INTERPRETATION]
  
  IF paciente responde "Não vou poder":
    → LLM interpreta a intenção
    → Oferecer reagendamento
    → Liberar slot
  
  IF paciente responde "Sim, confirmado":
    → Atualizar status
    → Enviar orientações finais
  
  IF paciente não responde:
    → Considerar "silêncio = confirmação"
    → Enviar última lembrança 2h antes
```

---

## FLUXO 9️⃣: Fila de Espera (RF24-25)

### 🎯 Objetivo
Maximizar ocupação da agenda.

### 🔄 Resumo

```
PACIENTE: "Quero esse horário mas não está disponível"
    ↓
AGENT: "Podemos colocar você na fila de espera?
        Se alguém cancelar, você é o primeiro
        a ser notificado!"
    ↓
PACIENTE: "Sim, coloca!"
    ↓
[INSERT Waitlist Entry]
    ↓
[WAIT for cancellation]
    ↓
[CANCELLATION detected]
    ↓
[AUTO-MATCH: Check waitlist for this slot]
    ↓
[ACTIVE NOTIFICATION]
    AGENT: "João! Ótima notícia! 🎉
            O horário de Seg 14:00 ficou
            disponível. Quer confirmar?"
    ↓
[IF sim: Proceder ao agendamento]
[IF não: Manter na fila]
```

---

## FLUXO 🔟: Cross-Selling (RF26-27)

### 🎯 Objetivo
Aumentar ticket médio com sugestões inteligentes.

### 🔄 Resumo

```
[APÓS AGENDAMENTO PRINCIPAL]

AGENT: "João, vi que é sua primeira
        hidratação. Posso sugerir?
        
        💡 Limpeza de Pele + Hidratação
        no mesmo dia = melhor resultado!
        
        Profissional: Maria (especialista)
        Próximo horário: Seg 15:30 (1h depois)
        Desconto combo: 20% OFF no segundo"

[IF interessado]
  → Buscar novo horário
  → Aplicar regra de combo
  → Confirmar duplo agendamento

[IF não interessado]
  → Sugerir complemento menor
  → Ex: "Creme pós-procedimento?"
```

---

## FLUXO 1️⃣1️⃣: Cobrança (RF28-29)

### 🎯 Objetivo
Integração segura com payment gateway.

### 🔄 Sequência

```
[AGENDAMENTO CONFIRMADO]
    ↓
[1] Gerar Link de Pagamento
    - Serviço: Limpeza de Pele
    - Valor: R$ 127,50 (com desconto)
    - Link PIX/Cartão: [https://...]
    - Validade: 24 horas
    
[2] Enviar ao Paciente
    "Para garantir seu horário,
     realize o pagamento de sinal:
     
     💳 PIX (copia e cola):
     00020126580014br.gov.bcb.pix...
     
     🔗 Ou clique aqui: [link]
     
     ⏰ Válido por 24 horas"

[3] Aguardar Webhook do Payment Gateway
    └─ Stripe/MercadoPago/etc envia
       webhook: payment.completed
    
[4] Callback Handler
    payment_id: "...",
    status: "completed",
    timestamp: "..."
    
    → UPDATE agendamento
      SET status = 'pagamento_confirmado'
    
    → Enviar confirmação final

[5] Pós-Pagamento
    "✅ Pagamento recebido!
     Seu agendamento está 100% garantido.
     Será um prazer atendê-lo! 😊"
```

---

## FLUXO 1️⃣2️⃣: Multimodalidade (RF31-32)

### 🎯 Objetivo
Suportar imagens e documentos.

### 🔄 Sequência

```
PACIENTE: [Envia foto de acne no rosto]
    ↓
AGENT: [Recebe imagem]
    ↓
[1] Validação:
    - Formato válido? ✓
    - Tamanho < 10MB? ✓
    - NSFW check? ✓
    
[2] Análise:
    - Armazenar em Cloud Storage
    - Extrair metadados
    - Descrição: "Imagem de acne moderada
                  em região frontal"
    
[3] Resposta:
    "Entendi! Pela imagem vejo que
     é acne moderada. Recomendo:
     
     1. Limpeza de Pele Profunda (R$ 150)
     2. Peeling Químico (R$ 180)
     3. Sessão com dermatologista (R$ 250)
     
     Quer saber mais sobre alguma opção?"

[4] Documentos (Formulários)
    AGENT: "Preciso que você preencha
            nossa ficha de anamnese.
            
            📄 Clique aqui para download"
    
    PACIENTE: [Clica, preenche, retorna]
    
    → Armazenar no dossiê do paciente
    → Notificar profissional
```

---

## 🎯 Resumo de Fluxos Críticos

| Fluxo | Criticidade | Tempo Real | Transacional |
|-------|-------------|-----------|----------------|
| Agendamento | 🔴 CRÍTICO | Sim | Sim (ACID) |
| Detecção de Crise | 🔴 CRÍTICO | Sim | Não |
| Cancelamento | 🟠 ALTO | Sim | Sim |
| Confirmação Ativa | 🟡 MÉDIO | Não (Async) | Não |
| Cross-Selling | 🟢 BAIXO | Sim | Não |

**Próximo**: Consulte [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md) para detalhes das regras parametrizadas.

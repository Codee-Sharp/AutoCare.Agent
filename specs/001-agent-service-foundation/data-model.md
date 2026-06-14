# Data Model: Fundação do Serviço de Agente

## ProcessRequest

- `contract_version`: string fixa `1.0`
- `paciente_id`: UUID, obrigatório, usado somente nas integrações autorizadas
- `sessao_id`: UUID, obrigatório, nunca registrado em claro
- `mensagem`: string sanitizada, não vazia, tamanho máximo configurável
- `contexto`: `ConversationContext` opcional, campos extras proibidos

## ConversationContext

- `nome_preferido`: string opcional, sem identificador legal
- `locale`: string opcional
- `timezone`: string opcional
- `resumo_sessao`: string opcional, sanitizado e limitado
- `resultado_autoritativo`: `AuthoritativeResult` opcional

CPF, pagamento, segredo, prompt, regra interna e histórico clínico são
proibidos.

## AgentState

- Request sanitizada e `request_id`
- Contexto temporário recuperado
- Node atual e intenção
- Indicadores de crise, handoff e falha segura
- Resposta do LLM validada
- Resultados de consulta autoritativa
- Ações propostas validadas

Transições principais:

`received -> validated -> session_loaded -> safety_checked`

- Crise: `safety_checked -> crisis_response -> completed`
- Normal: `safety_checked -> prompted -> classified -> llm_processed ->
  actions_validated -> session_saved -> completed`
- Falha insegura: qualquer node normal `-> safe_failure -> completed`

## ProcessResponse

- `contract_version`: string fixa `1.0`
- `sucesso`: boolean
- `resposta_texto`: string segura e não vazia
- `intencao`: enum conhecida
- `acoes_requeridas`: lista de `ProposedAction`
- `dossie_handoff`: opcional
- `alerta_crise`: opcional
- `request_id`: UUID

## ProposedAction

- `action_id`: UUID gerado pelo agente para deduplicação externa
- `tipo`: enum das seis ações suportadas
- `mode`: `query` ou `propose`
- `parametros`: objeto específico por tipo, sem campos extras
- `request_id`: UUID de correlação

Regras:

- `confirmar_agendamento` e `cancelar_agendamento` sempre usam `mode=propose`.
- Ações desconhecidas ou parâmetros inválidos são descartados e causam resposta
  segura.
- A proposta nunca representa confirmação de execução.

## CrisisAlert

- `tipo`: enum de categorias de risco
- `severidade`: enum `high` ou `critical`
- `orientacao_codigo`: código de orientação configurada
- `escalonamento_humano`: sempre `true`

Não contém trecho da mensagem nem avaliação diagnóstica.

## HandoffDossier

- `motivo`: enum conhecido
- `intencao`: intenção conhecida ou `unknown`
- `resumo_sanitizado`: resumo limitado e sem dados proibidos
- `acoes_pendentes`: propostas validadas

## SessionContext

- `contract_version`: string fixa `1.0`
- `sessao_hash`: hash não reversível usado na chave
- `resumo_sanitizado`: string limitada
- `ultima_intencao`: enum conhecida
- `acoes_pendentes`: lista limitada de propostas
- `updated_at`: timestamp UTC
- `expires_in_seconds`: TTL configurável, padrão `1800`

O contexto expira automaticamente e nunca contém mensagem completa.

## LLMResult

- `resposta_texto`: string
- `intencao`: enum conhecida
- `acoes_propostas`: lista limitada
- `solicita_handoff`: boolean

Todo conteúdo é tratado como não confiável até validação.

## ToolResult

- `contract_version`: string fixa `1.0`
- `request_id`: UUID
- `status`: `success`, `unavailable`, `timeout` ou `invalid_response`
- `data`: payload tipado opcional
- `error_code`: código sanitizado opcional

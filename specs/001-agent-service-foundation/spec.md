# Feature Specification: Fundação do Serviço de Agente

**Feature Branch**: `001-agent-service-foundation`

**Created**: 2026-06-13

**Status**: Implemented with simplified scope

**Input**: User description: "Entregar uma fundação executável, testável e extensível para um serviço conversacional seguro, integrado exclusivamente à aplicação interna, com contexto temporário, detecção de crise, handoff humano, ações estruturadas, observabilidade e falhas seguras."

## Clarifications

### Session 2026-06-14

- Q: A arquitetura pode ser simplificada considerando que o Agent fica atrás da
  aplicação interna e responde apenas pelo processamento/orquestração da LLM?
  → A: Sim. A implementação é stateless, usa um `Orchestrator` apoiado por um
  LangGraph enxuto e remove Redis e clientes REST internos. A aplicação interna
  envia contexto, mantém estado e executa ações. O
  [plano atualizado](./plan.md) é a fonte de verdade técnica desta alteração de
  escopo.

### Session 2026-06-13

- Q: Como ações críticas de agendamento devem funcionar? → A: O agente apenas propõe ações estruturadas; a aplicação interna valida, autoriza e executa.
- Q: Como mensagens com possível crise, mas sem sinal inequívoco, devem ser tratadas? → A: Solicitar uma pergunta curta de confirmação antes de escalar.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversa segura e útil (Priority: P1)

Como paciente, quero enviar uma mensagem e receber uma resposta conversacional
segura, contextualizada e rastreável, para obter orientação administrativa sem
que o agente invente fatos ou realize ações críticas por conta própria.

**Why this priority**: É o fluxo principal que entrega valor e estabelece os
limites de segurança do agente.

**Independent Test**: Pode ser testado enviando uma mensagem administrativa
com identificadores válidos e verificando que a resposta contém texto,
intenção, ações estruturadas e identificador de rastreio, sem confirmação ou
fato crítico inventado.

**Acceptance Scenarios**:

1. **Given** uma mensagem válida e sem risco, **When** o paciente solicita ajuda administrativa, **Then** o agente retorna uma resposta segura, uma intenção identificada, ações requeridas estruturadas e um identificador único da solicitação.
2. **Given** uma conversa anterior da mesma sessão, **When** o paciente envia uma nova mensagem, **Then** o agente usa somente o contexto temporário necessário para manter a continuidade.
3. **Given** uma pergunta sobre preço, desconto, disponibilidade ou confirmação, **When** não há resposta autoritativa da aplicação interna, **Then** o agente informa que não pode confirmar o fato e não o inventa.

---

### User Story 2 - Interrupção por crise (Priority: P1)

Como paciente em possível situação de crise, quero que sinais de risco sejam
priorizados imediatamente, para receber orientação segura e escalonamento
humano sem continuar o fluxo administrativo normal.

**Why this priority**: A segurança do paciente tem precedência sobre qualquer
outra capacidade do serviço.

**Independent Test**: Pode ser testado enviando uma mensagem com sinal
inequívoco de crise e verificando que o fluxo normal é interrompido, nenhuma
ação administrativa é proposta e um alerta estruturado é retornado.

**Acceptance Scenarios**:

1. **Given** uma mensagem com sinal de crise, **When** ela é processada, **Then** o agente interrompe o fluxo normal imediatamente, retorna orientação segura, produz alerta estruturado e solicita escalonamento humano.
2. **Given** uma mensagem de crise, **When** o alerta é gerado, **Then** o retorno e os registros não incluem conteúdo sensível desnecessário.
3. **Given** uma mensagem ambígua com possível sinal de crise, **When** ela é processada, **Then** o agente interrompe ações administrativas, não chama tools e faz uma única pergunta curta de confirmação antes de decidir pelo escalonamento.

---

### User Story 3 - Solicitação de atendimento humano (Priority: P2)

Como paciente, quero poder pedir atendimento humano explicitamente, para que
minha solicitação e o contexto mínimo relevante sejam encaminhados a uma
pessoa.

**Why this priority**: O handoff preserva confiança e segurança quando o agente
não deve ou não consegue concluir o atendimento.

**Independent Test**: Pode ser testado com um pedido explícito de atendimento
humano e verificação de um dossiê estruturado, mínimo e sem dados proibidos.

**Acceptance Scenarios**:

1. **Given** um pedido explícito de atendimento humano, **When** o agente processa a mensagem, **Then** ele retorna um dossiê de handoff estruturado com motivo e contexto mínimo necessário.
2. **Given** uma falha que impede resposta segura, **When** o agente não consegue concluir o fluxo, **Then** ele oferece handoff humano e retorna uma resposta segura.

---

### User Story 4 - Execução por aplicação interna (Priority: P2)

Como aplicação interna, quero receber ações críticas estruturadas e validadas,
para decidir e executar operações usando as fontes autoritativas existentes.

**Why this priority**: Mantém regras de negócio e execução crítica fora do
agente, reduzindo risco operacional.

**Independent Test**: Pode ser testado fazendo o agente propor operações de
consulta e agendamento e verificando que somente ações reconhecidas,
estruturadas e validadas são retornadas.

**Acceptance Scenarios**:

1. **Given** uma intenção que exige consulta ou operação, **When** o agente prepara a resposta, **Then** ele representa a necessidade como uma ação estruturada para a aplicação interna.
2. **Given** uma ação crítica inventada, desconhecida ou inválida, **When** ela é validada, **Then** o agente a bloqueia e retorna um resultado seguro.
3. **Given** indisponibilidade ou resposta inválida de uma fonte autoritativa, **When** a ação é processada, **Then** nenhuma confirmação é emitida e o paciente recebe uma resposta segura.

---

### User Story 5 - Operação observável e verificável (Priority: P3)

Como equipe operadora, quero verificar saúde, rastrear solicitações e entender
falhas sem expor dados sensíveis, para operar o serviço com segurança.

**Why this priority**: A operação confiável depende de diagnóstico rápido e
privacidade preservada.

**Independent Test**: Pode ser testado consultando os indicadores de saúde e
inspecionando registros de uma solicitação normal, uma crise e uma falha
externa.

**Acceptance Scenarios**:

1. **Given** uma instância em execução, **When** sua condição básica é consultada, **Then** ela informa se está ativa.
2. **Given** dependências necessárias disponíveis ou indisponíveis, **When** a prontidão é consultada, **Then** ela reflete corretamente se a instância pode atender solicitações.
3. **Given** qualquer solicitação processada, **When** seus registros são inspecionados, **Then** eles permitem rastrear etapas, duração e resultado sem revelar mensagem completa, prompt, segredo ou dado pessoal sensível.

### Edge Cases

- Mensagem vazia, composta somente por espaços ou acima do limite permitido.
- Identificadores de paciente ou sessão ausentes, inválidos ou malformados.
- Contexto opcional contendo campos excessivos, inesperados ou proibidos.
- Mensagem ambígua que pode indicar risco; o agente interrompe ações administrativas, não chama tools e faz uma única pergunta curta de confirmação antes de decidir pelo escalonamento.
- Pedido de atendimento humano junto com sinal de crise; a crise tem prioridade.
- Resposta conversacional ausente, malformada ou com ação desconhecida.
- Tentativa do modelo de confirmar preço, desconto, disponibilidade ou operação sem fonte autoritativa.
- Fonte autoritativa indisponível, lenta ou retornando conteúdo inválido.
- Armazenamento temporário indisponível ou contendo contexto inválido.
- Solicitações repetidas ou concorrentes para a mesma sessão.

### Safety, Privacy & Failure Modes *(mandatory)*

- **Safety/Handoff Impact**: Sinais de crise interrompem imediatamente o fluxo
  normal, produzem alerta estruturado e solicitam escalonamento humano. Pedidos
  explícitos de atendimento humano e situações sem resposta segura produzem
  dossiê de handoff. O agente não fornece diagnóstico médico.
- **Data Exposure**: Somente identificadores necessários, mensagem sanitizada e
  contexto mínimo da conversa podem ser usados. CPF completo, dados de
  pagamento, segredos, regras internas, mensagens completas em registros e
  informações clínicas sensíveis desnecessárias nunca podem ser expostos.
- **Authoritative Sources**: A aplicação interna é a única autoridade para
  preços, descontos, disponibilidade, serviços, agendamentos e execução de
  ações críticas. O agente nunca acessa armazenamento de negócio diretamente.
- **Failure Behavior**: Falhas, timeouts e respostas inválidas de dependências
  resultam em resposta segura, ausência de confirmação crítica e handoff quando
  necessário. Solicitações repetidas não podem produzir confirmações duplicadas
  pelo agente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST aceitar solicitações contendo identificador do paciente, identificador da sessão, mensagem e contexto opcional mínimo.
- **FR-002**: O sistema MUST validar e sanitizar todo dado recebido antes de utilizá-lo.
- **FR-003**: O sistema MUST rejeitar mensagens vazias ou acima do limite máximo configurado com resposta segura e clara.
- **FR-004**: O sistema MUST retornar, para toda solicitação aceita, sucesso, texto de resposta, intenção, lista de ações estruturadas e identificador único da solicitação.
- **FR-005**: O sistema MUST incluir alerta de crise estruturado quando detectar risco e MUST omiti-lo quando não houver risco detectado.
- **FR-006**: O sistema MUST incluir dossiê de handoff estruturado quando houver pedido explícito de atendimento humano ou impossibilidade de responder com segurança.
- **FR-007**: O sistema MUST interromper o processamento conversacional normal imediatamente após detectar crise.
- **FR-008**: O sistema MUST priorizar crise sobre pedidos administrativos e sobre handoff comum.
- **FR-008A**: O sistema MUST tratar possível crise ambígua fazendo uma única pergunta curta de confirmação, sem executar ações administrativas ou chamar tools até receber a resposta.
- **FR-009**: O sistema MUST classificar a intenção da mensagem antes de construir a resposta final.
- **FR-010**: O sistema MUST usar uma capacidade conversacional substituível sem acoplar o domínio a um fornecedor específico.
- **FR-011**: O sistema MUST oferecer um modo determinístico de processamento para testes sem dependências externas.
- **FR-012**: O sistema MUST tratar indisponibilidade, timeout e conteúdo inválido da capacidade conversacional com resposta segura.
- **FR-013**: O sistema MUST validar toda ação proposta antes de retorná-la à aplicação interna.
- **FR-014**: O sistema MUST bloquear ações desconhecidas, malformadas ou sem parâmetros obrigatórios.
- **FR-015**: O sistema MUST apenas propor toda ação crítica como ação estruturada; a aplicação interna MUST validar, autorizar e executar a ação.
- **FR-016**: O sistema MUST NOT inventar ou confirmar preços, descontos, disponibilidade, serviços ou resultado de operações.
- **FR-017**: O sistema MUST permitir ações estruturadas para buscar disponibilidade, consultar serviço, validar desconto, confirmar agendamento, listar agendamentos e cancelar agendamento.
- **FR-018**: O sistema MUST consultar fatos somente por meio das fontes autoritativas da aplicação interna e MUST apenas propor ações críticas para validação, autorização e execução pela aplicação interna.
- **FR-019**: O sistema MUST validar dados enviados e recebidos de toda fonte autoritativa.
- **FR-020**: O sistema MUST aplicar limite de duração explícito a toda chamada externa.
- **FR-021**: O sistema MUST propagar o identificador da solicitação em toda interação com fonte autoritativa.
- **FR-022**: O sistema MUST manter somente contexto temporário e mínimo necessário por sessão.
- **FR-023**: O sistema MUST continuar com resposta segura quando o contexto temporário estiver indisponível ou inválido.
- **FR-024**: O sistema MUST minimizar os dados apresentados à capacidade conversacional.
- **FR-025**: O sistema MUST NOT apresentar CPF completo, dados de pagamento, segredos ou regras internas à capacidade conversacional ou aos registros operacionais.
- **FR-026**: O sistema MUST NOT registrar mensagens completas, prompts completos, tokens ou informações clínicas sensíveis.
- **FR-027**: O sistema MUST produzir registros estruturados com identificador da solicitação, sessão anonimizada, etapa atual, intenção, duração, resultado externo e motivo não sensível de crise ou handoff.
- **FR-028**: O sistema MUST informar separadamente se uma instância está ativa e se está pronta para atender solicitações.
- **FR-029**: O domínio MUST permanecer independente de mecanismos de entrega, armazenamento temporário e fornecedores externos.
- **FR-030**: O sistema MUST ser verificável sem acesso real à rede.
- **FR-031**: O sistema MUST NOT acessar diretamente dados persistentes da aplicação interna, processar pagamentos ou assumir autoridade sobre regras de negócio.
- **FR-032**: O sistema MUST fornecer orientação não diagnóstica e solicitar handoff humano quando uma resposta puder comprometer a segurança do paciente.

### Key Entities

- **Solicitação do Agente**: Pedido de processamento identificado, associado a paciente e sessão, contendo mensagem e contexto opcional mínimo.
- **Resposta do Agente**: Resultado rastreável contendo estado de sucesso, resposta textual, intenção, ações requeridas e, quando aplicável, crise ou handoff.
- **Ação Estruturada**: Solicitação tipada para consulta ou operação cuja decisão e execução pertencem à aplicação interna.
- **Contexto Temporário de Sessão**: Informações mínimas e não críticas usadas exclusivamente para continuidade da conversa.
- **Alerta de Crise**: Registro estruturado e não sensível que interrompe o fluxo normal e solicita escalonamento humano.
- **Dossiê de Handoff**: Resumo mínimo e estruturado para transferência do atendimento a uma pessoa.
- **Resultado Externo**: Resultado validado de uma consulta à fonte autoritativa, incluindo sucesso, falha ou indisponibilidade.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das mensagens de crise do conjunto de validação interrompem o fluxo normal e produzem alerta estruturado e solicitação de escalonamento humano.
- **SC-002**: 100% dos pedidos explícitos de atendimento humano do conjunto de validação produzem dossiê de handoff.
- **SC-003**: 100% das tentativas validadas de inventar ação crítica, preço, desconto, disponibilidade ou confirmação são bloqueadas antes da resposta final.
- **SC-004**: 100% dos cenários de indisponibilidade, timeout ou resposta inválida das dependências retornam resposta segura sem confirmação crítica indevida.
- **SC-005**: 100% dos registros do conjunto de auditoria omitem mensagens completas, prompts, CPF completo, dados de pagamento, segredos e informações clínicas sensíveis.
- **SC-006**: Uma solicitação administrativa normal recebe resposta em até 5 segundos em pelo menos 95% das execuções quando as dependências estão disponíveis.
- **SC-007**: A condição ativa e a prontidão operacional podem ser determinadas em até 2 segundos em pelo menos 99% das consultas.
- **SC-008**: Todos os fluxos obrigatórios podem ser verificados em ambiente isolado, sem acesso real à rede.
- **SC-009**: Em avaliação de aceitação, pelo menos 90% das solicitações administrativas suportadas recebem uma resposta compreensível ou um encaminhamento humano apropriado na primeira tentativa.

## Assumptions

- A aplicação interna autentica e autoriza pacientes e operadores antes de encaminhar solicitações ao agente.
- A aplicação interna permanece responsável por persistência crítica, regras de negócio, pagamentos e execução final de ações.
- O contexto recebido já foi reduzido ao necessário, mas o agente ainda valida e remove campos proibidos.
- A política detalhada de retenção do contexto temporário será definida no planejamento, adotando retenção curta e configurável.
- A primeira entrega cobre conversas administrativas e encaminhamento seguro; diagnóstico médico e fluxos completos de produção permanecem fora do escopo.
- Os requisitos técnicos, estrutura de projeto e ferramentas indicados na descrição original serão tratados como restrições obrigatórias no plano de implementação.

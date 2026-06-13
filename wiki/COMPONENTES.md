# 🔧 COMPONENTES E INTERFACES

## Índice

1. [Modelos de Dados](#1-modelos-de-dados)
2. [APIs do Backend](#2-apis-do-backend)
3. [Estrutura de Eventos](#3-estrutura-de-eventos)
4. [Tools do Agent](#4-tools-do-agent)
5. [Response Patterns](#5-response-patterns)

---

## 1. Modelos de Dados

### 1.1 Paciente

```typescript
interface Paciente {
  id: UUID;
  nome: string;
  cpf: string; // criptografado
  email: string;
  telefone: string;
  
  // Perfil
  data_nascimento?: Date;
  genero?: 'M' | 'F' | 'Outro';
  endereco?: string;
  
  // Status
  status: 'ativo' | 'inativo' | 'banido';
  banido_ate?: Date;
  primeira_visita: boolean;
  
  // Histórico
  total_agendamentos_realizados: number;
  total_gasto: number;
  ultimo_agendamento?: Date;
  
  // Preferências
  especialidade_preferida?: string;
  servicos_preferidos?: string[];
  frequencia_estimada_dias?: number;
  
  // Contratos
  aceita_marketing: boolean;
  aceita_lembretes: boolean;
  preferencia_comunicacao: 'sms' | 'email' | 'whatsapp';
  
  // Admin
  nota_interna?: string;
  criado_em: Date;
  atualizado_em: Date;
  deletado_em?: Date;
}
```

### 1.2 Agendamento

```typescript
interface Agendamento {
  id: UUID;
  
  // Referências
  paciente_id: UUID;
  servico_id: UUID;
  profissional_id: UUID;
  
  // Data e Hora
  data_hora: DateTime; // ISO 8601
  duracao_minutos: number;
  
  // Status
  status: 'pendente' | 'confirmado' | 'realizado' | 'cancelado';
  protocolo: string; // Único: AG-YYYYMMDD-NNN
  
  // Pagamento
  valor_original: decimal;
  valor_desconto?: decimal;
  valor_final: decimal;
  status_pagamento: 'nao_pago' | 'sinal_pago' | 'pago';
  pagamento_id?: string; // ID externo Stripe/MercadoPago
  
  // Dados Complementares
  dados_adicionais?: {
    alergias?: string[];
    medicamentos?: string[];
    observacoes?: string;
    imagens_referencia?: string[];
  };
  
  // Admin
  criado_em: DateTime;
  atualizado_em: DateTime;
  cancelado_em?: DateTime;
  realizado_em?: DateTime;
  
  // Notas
  nota_profissional?: string;
  nota_paciente?: string;
}
```

### 1.3 Serviço

```typescript
interface Servico {
  id: UUID;
  nome: string;
  descricao: string;
  categoria: 'estética' | 'psicologia' | 'psiquiatria' | 'salao' | 'outro';
  
  // Duração e Preço
  duracao_minutos: number;
  preco_base: decimal;
  
  // Detalhes
  beneficios: string[];
  contraindicacoes?: string[];
  orientacoes: {
    pre?: string;
    pos?: string;
  };
  
  // Disponibilidade
  ativo: boolean;
  profissionais_habilitados: UUID[];
  requer_confirmacao_pagamento: boolean;
  
  // Metadados
  criado_em: DateTime;
  atualizado_em: DateTime;
}
```

### 1.4 Lock Temporário

```typescript
interface LockTemporario {
  id: UUID;
  agendamento_id?: UUID; // null se ainda é lock
  paciente_id: UUID;
  profissional_id: UUID;
  servico_id: UUID;
  data_hora: DateTime;
  
  criado_em: DateTime;
  expira_em: DateTime;
  ttl_segundos: number; // default: 300 (5 min)
  
  // Metadados
  origem: 'agent' | 'web' | 'app';
}
```

### 1.5 Desconto

```typescript
interface Desconto {
  id: UUID;
  agendamento_id: UUID;
  
  // Valor
  percentual?: number;
  valor_fixo?: decimal;
  
  // Origem
  tipo: 'automatico' | 'manual' | 'cupon';
  nome_promocao: string;
  
  // Aprovação
  aprovado: boolean;
  aprovado_por?: string; // UUID ou email
  motivo_rejeicao?: string;
  
  criado_em: DateTime;
  atualizado_em: DateTime;
}
```

### 1.6 Lembrete

```typescript
interface Lembrete {
  id: UUID;
  agendamento_id: UUID;
  
  // Tipo
  tipo: '24h' | '48h' | 'dia_anterior' | 'uma_hora_antes';
  
  // Status
  status: 'pendente' | 'enviado' | 'falha' | 'ignorado';
  tentativas: number;
  
  // Canal
  canal: 'sms' | 'email' | 'whatsapp' | 'push';
  
  // Conteúdo
  titulo: string;
  corpo: string;
  cta?: string; // Call to action
  
  // Detalhes
  enviado_em?: DateTime;
  visto_em?: DateTime;
  resposta_paciente?: {
    tipo: 'confirmacao' | 'cancelamento' | 'reagendamento' | 'ignorado';
    texto?: string;
    timestamp: DateTime;
  };
  
  criado_em: DateTime;
}
```

### 1.7 Waitlist (Fila de Espera)

```typescript
interface Waitlist {
  id: UUID;
  paciente_id: UUID;
  servico_id: UUID;
  profissional_id?: UUID;
  
  // Preferência
  data_hora_preferida?: DateTime;
  periodo_preferido?: 'manhã' | 'tarde' | 'qualquer';
  
  // Status
  status: 'ativo' | 'notificado' | 'cancelado' | 'expirado';
  notificacoes_tentadas: number;
  
  // Timestamp
  criado_em: DateTime;
  expira_em: DateTime;
  notificado_em?: DateTime;
}
```

### 1.8 Dossiê de Chat (Handoff)

```typescript
interface DossieCha {
  id: UUID;
  protocolo_chat: string; // CHAT-YYYYMMDD-NNN
  paciente_id: UUID;
  
  // Contexto
  intent_principal: string;
  sentimento: 'positivo' | 'neutro' | 'negativo' | 'ansioso' | 'critico';
  
  // Histórico
  mensagens: Array<{
    timestamp: DateTime;
    autor: 'paciente' | 'agent';
    tipo: 'texto' | 'imagem' | 'documento';
    conteudo: string;
  }>;
  
  // Resumo Estruturado
  resumo: {
    problema: string;
    tentativas_resolucao: string[];
    proximos_passos: string[];
    dados_coletados: Record<string, any>;
    urgencia: 'baixa' | 'média' | 'alta' | 'crítica';
  };
  
  // Status
  status: 'aberto' | 'em_atendimento' | 'resolvido' | 'escalado';
  atendente_id?: UUID;
  
  criado_em: DateTime;
  fechado_em?: DateTime;
}
```

### 1.9 Alerta de Crise

```typescript
interface AlertaCrise {
  id: UUID;
  dossiê_id?: UUID;
  paciente_id: UUID;
  
  // Tipo de Crise
  tipo: 'suicidio' | 'automutilacao' | 'abusor' | 'agressividade' | 'outro';
  severidade: 'moderada' | 'severa' | 'critica';
  score_confianca: number; // 0-1
  
  // Texto Original
  texto_original: string;
  
  // Ações Tomadas
  protocolo_ativado: boolean;
  contatos_emergencia_enviados: boolean;
  staff_notificados: boolean;
  
  // Resposta
  respondido_por?: string; // Nome do staff
  respondido_em?: DateTime;
  resposta?: string;
  
  criado_em: DateTime;
}
```

---

## 2. APIs do Backend

### 2.1 API de Pacientes

```typescript
/**
 * GET /api/pacientes/{id}
 * Recupera dados do paciente
 */
interface GetPacienteRequest {
  id: UUID;
}

interface GetPacienteResponse {
  paciente: Paciente;
  historico_recente?: Agendamento[];
}

/**
 * POST /api/pacientes
 * Cria novo paciente (ou retorna existente se CPF já cadastrado)
 */
interface CreatePacienteRequest {
  nome: string;
  cpf: string;
  email: string;
  telefone: string;
}

interface CreatePacienteResponse {
  paciente: Paciente;
  novo: boolean; // true se criado, false se já existia
}

/**
 * PATCH /api/pacientes/{id}
 * Atualiza dados do paciente
 */
interface UpdatePacienteRequest {
  nome?: string;
  email?: string;
  telefone?: string;
  aceita_marketing?: boolean;
  preferencia_comunicacao?: string;
}

interface UpdatePacienteResponse {
  paciente: Paciente;
}
```

### 2.2 API de Disponibilidade

```typescript
/**
 * POST /api/agendamentos/disponibilidade
 * Busca horários disponíveis
 */
interface BuscaDisponibilidadeRequest {
  servico_id: UUID;
  data_inicio: Date; // YYYY-MM-DD
  data_fim: Date; // YYYY-MM-DD
  profissional_id?: UUID;
  periodo?: 'manhã' | 'tarde' | 'noite';
}

interface SlotDisponivel {
  profissional_id: UUID;
  profissional_nome: string;
  data_hora: DateTime;
  duracao_minutos: number;
}

interface BuscaDisponibilidadeResponse {
  slots_disponiveis: SlotDisponivel[];
  total: number;
}
```

### 2.3 API de Agendamento

```typescript
/**
 * POST /api/agendamentos/confirmar
 * Confirma agendamento (transação crítica)
 */
interface ConfirmarAgendamentoRequest {
  paciente_id: UUID;
  servico_id: UUID;
  profissional_id: UUID;
  data_hora: DateTime;
  
  // Dados obrigatórios
  cpf?: string; // Se não existe no BD
  email?: string; // Se não existe no BD
  
  // Desconto (opcional)
  desconto_id?: UUID;
  codigo_promocional?: string;
  
  // Metadados
  origem: 'agent' | 'web' | 'app';
}

interface AgendamentoConfirmado {
  id: UUID;
  protocolo: string;
  status: 'confirmado';
  valor_final: decimal;
  data_hora: DateTime;
  orientacoes_pre: string[];
  orientacoes_pos: string[];
}

interface ConfirmarAgendamentoResponse {
  agendamento: AgendamentoConfirmado;
  sucesso: true;
}

/**
 * GET /api/agendamentos/{paciente_id}
 * Lista agendamentos do paciente
 */
interface ListarAgendamentosResponse {
  proximos: Agendamento[]; // Futuros
  historico: Agendamento[]; // Últimos 10 realizados
  total_futuro: number;
}

/**
 * DELETE /api/agendamentos/{id}
 * Cancela agendamento
 */
interface CancelarAgendamentoRequest {
  id: UUID;
  motivo?: string;
}

interface CancelarAgendamentoResponse {
  sucesso: true;
  protocolo_cancelamento: string;
  reembolso?: {
    percentual: number;
    valor: decimal;
    data_processamento: Date;
  };
}
```

### 2.4 API de Descontos

```typescript
/**
 * POST /api/descontos/validar
 * Valida elegibilidade para desconto
 */
interface ValidarDescontoRequest {
  paciente_id: UUID;
  servico_id: UUID;
  motivo?: string; // Ex: "primeira_visita", "lealdade"
}

interface ValidarDescontoResponse {
  elegivel: boolean;
  desconto_percentual?: number;
  desconto_fixo?: decimal;
  valor_original?: decimal;
  valor_com_desconto?: decimal;
  condicoes?: {
    descricao: string;
    validade: Date;
    requer_agendamento_imediato?: boolean;
  };
  motivo_ineligibilidade?: string;
}
```

### 2.5 API de Catálogo

```typescript
/**
 * GET /api/servicos
 * Lista todos os serviços
 */
interface ListarServicosResponse {
  servicos: Servico[];
}

/**
 * GET /api/servicos/{id}
 * Detalhes de um serviço
 */
interface GetServicoResponse {
  servico: Servico;
  profissionais: Array<{
    id: UUID;
    nome: string;
    especialidade: string;
  }>;
  preco_medio: decimal;
}

/**
 * GET /api/servicos/buscar?termo={termo}
 * Busca serviço por nome/descrição
 */
interface BuscaServicoResponse {
  resultados: Servico[];
}
```

### 2.6 API de Pagamento

```typescript
/**
 * POST /api/pagamentos/criar-link
 * Gera link/código PIX para pagamento
 */
interface CriarLinkPagamentoRequest {
  agendamento_id: UUID;
  valor: decimal;
  tipo_pagamento: 'sinal' | 'integral';
  metodos_aceitos: ('pix' | 'cartao' | 'boleto')[];
}

interface LinkPagamento {
  id: string; // ID da transação
  link?: string; // URL do checkout
  qr_code_pix?: string;
  codigo_pix?: string;
  validade: DateTime;
  instrucoes: string;
}

interface CriarLinkPagamentoResponse {
  pagamento: LinkPagamento;
}

/**
 * Webhook: POST /api/webhooks/pagamento
 * Recebe confirmação do gateway (Stripe, MercadoPago, etc)
 */
interface WebhookPagamentoRequest {
  id: string; // Payment ID
  status: 'completed' | 'failed' | 'cancelled';
  timestamp: DateTime;
  agendamento_id: UUID;
  valor: decimal;
  metodo: 'pix' | 'cartao' | 'boleto';
}

interface WebhookPagamentoResponse {
  sucesso: true;
}
```

### 2.7 API de Lembretes

```typescript
/**
 * POST /api/lembretes/criar
 * Cria lembrete para agendamento
 */
interface CriarLembreteRequest {
  agendamento_id: UUID;
  tipo: '24h' | '48h' | 'dia_anterior';
  canais: ('sms' | 'email' | 'whatsapp')[];
}

interface CriarLembreteResponse {
  lembrete: Lembrete;
}

/**
 * POST /api/lembretes/{id}/registrar-resposta
 * Registra resposta do paciente ao lembrete
 */
interface RegistrarRespostaLembreteRequest {
  resposta_tipo: 'confirmacao' | 'cancelamento' | 'reagendamento';
  texto?: string;
}

interface RegistrarRespostaLembreteResponse {
  sucesso: true;
}
```

---

## 3. Estrutura de Eventos

### 3.1 Event Emitter Pattern

```typescript
interface Event {
  id: UUID;
  tipo: string;
  timestamp: DateTime;
  payload: Record<string, any>;
  origem: 'agent' | 'api' | 'webhook';
}

/**
 * Eventos Principais
 */
enum EventoTipo {
  // Agendamento
  AGENDAMENTO_CRIADO = 'agendamento.criado',
  AGENDAMENTO_CONFIRMADO = 'agendamento.confirmado',
  AGENDAMENTO_CANCELADO = 'agendamento.cancelado',
  AGENDAMENTO_REALIZADO = 'agendamento.realizado',
  
  // Pagamento
  PAGAMENTO_CONFIRMADO = 'pagamento.confirmado',
  PAGAMENTO_FALHOU = 'pagamento.falhou',
  
  // Lembrete
  LEMBRETE_ENVIADO = 'lembrete.enviado',
  LEMBRETE_RESPONDIDO = 'lembrete.respondido',
  
  // Crise
  CRISE_DETECTADA = 'crise.detectada',
  CRISE_RESPONDIDA = 'crise.respondida',
  
  // Chat
  CHAT_INICIADO = 'chat.iniciado',
  CHAT_TRANSFERIDO = 'chat.transferido',
}
```

### 3.2 Listeners (Exemplo)

```typescript
// Email Service
eventEmitter.on(EventoTipo.AGENDAMENTO_CONFIRMADO, (evento) => {
  enviarEmailConfirmacao(evento.payload.agendamento);
});

// SMS Service
eventEmitter.on(EventoTipo.LEMBRETE_ENVIADO, (evento) => {
  enviarSMS(evento.payload.paciente, evento.payload.mensagem);
});

// Histórico Service
eventEmitter.on('*', (evento) => {
  registrarHistoricoInteracao(evento);
});

// Alert Service
eventEmitter.on(EventoTipo.CRISE_DETECTADA, (evento) => {
  notificarEquipeClinica(evento.payload);
  dispararSOS(evento.payload.paciente_id);
});
```

---

## 4. Tools do Agent

### 4.1 Tool: Buscar Disponibilidade

```typescript
interface ToolBuscaDisponibilidade {
  name: 'buscar_disponibilidade';
  description: 'Busca horários disponíveis para agendamento';
  parameters: {
    servico_id: string; // UUID
    data_inicio?: string; // YYYY-MM-DD
    data_fim?: string; // YYYY-MM-DD
    profissional_id?: string; // UUID
    periodo?: string; // 'manhã', 'tarde', 'qualquer'
  };
}

// Resposta esperada
interface ToolResposta {
  sucesso: boolean;
  slots?: Array<{
    id: string;
    data: string; // "Seg, 16/jun"
    hora: string; // "14:00"
    profissional: string; // "Maria (Esteticista)"
    duracao_minutos: number;
  }>;
  total?: number;
  mensagem: string; // Para comunicação ao paciente
}
```

### 4.2 Tool: Validar Desconto

```typescript
interface ToolValidarDesconto {
  name: 'validar_desconto';
  description: 'Valida elegibilidade para desconto';
  parameters: {
    paciente_id: string;
    servico_id: string;
    motivo?: string;
  };
}

// Resposta
interface RespostaDesconto {
  elegivel: boolean;
  desconto_percentual?: number;
  mensagem: string; // "Você ganhou 15% OFF!"
  condicoes?: string; // "Válido apenas se agendar agora"
}
```

### 4.3 Tool: Confirmar Agendamento

```typescript
interface ToolConfirmarAgendamento {
  name: 'confirmar_agendamento';
  description: 'Confirma um agendamento com garantia de não double-booking';
  parameters: {
    paciente_id: string;
    servico_id: string;
    profissional_id: string;
    data_hora: string; // ISO 8601
    cpf?: string;
    email?: string;
    desconto_id?: string;
  };
}

// Resposta
interface RespostaConfirmacao {
  sucesso: boolean;
  protocolo?: string; // "AG-20260616-001"
  mensagem: string;
  detalhes?: {
    data: string;
    hora: string;
    profissional: string;
    valor: number;
    orientacoes: string[];
  };
}
```

### 4.4 Tool: Consultar Serviço

```typescript
interface ToolConsultarServico {
  name: 'consultar_servico';
  description: 'Recupera informações sobre um serviço específico';
  parameters: {
    servico_id?: string;
    nome_servico?: string;
  };
}

// Resposta
interface RespostaServico {
  encontrado: boolean;
  servico?: {
    nome: string;
    preco: number;
    duracao_minutos: number;
    beneficios: string[];
    orientacoes_pre: string;
    orientacoes_pos: string;
  };
  mensagem: string;
}
```

### 4.5 Tool: Listar Agendamentos do Paciente

```typescript
interface ToolListarAgendamentos {
  name: 'listar_agendamentos';
  description: 'Lista agendamentos atuais do paciente';
  parameters: {
    paciente_id: string;
  };
}

// Resposta
interface RespostaAgendamentos {
  proximos: Array<{
    protocolo: string;
    servico: string;
    data: string; // "Seg, 16/jun"
    hora: string;
    profissional: string;
    valor: number;
  }>;
  historico: Array<{
    servico: string;
    data: string;
    status: 'realizado' | 'cancelado';
  }>;
}
```

### 4.6 Tool: Cancelar Agendamento

```typescript
interface ToolCancelarAgendamento {
  name: 'cancelar_agendamento';
  description: 'Cancela um agendamento com validações de regra';
  parameters: {
    agendamento_id: string;
    motivo?: string;
  };
}

// Resposta
interface RespostaCancelamento {
  sucesso: boolean;
  protocolo_cancelamento?: string;
  mensagem: string;
  reembolso?: {
    percentual: number;
    valor: number;
    observacao: string;
  };
}
```

---

## 5. Response Patterns

### 5.1 Padrão de Erro

```typescript
interface ErrorResponse {
  erro: true;
  codigo: string; // Ex: 'PACIENTE_NAO_ENCONTRADO'
  mensagem: string; // User-friendly
  detalhes?: {
    campo?: string;
    esperado?: any;
    recebido?: any;
  };
  timestamp: DateTime;
  request_id: UUID;
}
```

### 5.2 Padrão de Sucesso

```typescript
interface SuccessResponse<T> {
  sucesso: true;
  dados: T;
  timestamp: DateTime;
  request_id: UUID;
}
```

### 5.3 Padrão de Validação

```typescript
interface ValidationError {
  campo: string;
  mensagem: string;
  tipo_erro: 'obrigatorio' | 'formato' | 'valor' | 'regra_negocio';
  valor_recebido?: any;
}

interface ValidationResponse {
  valido: false;
  erros: ValidationError[];
}
```

---

**Próximo**: Consulte [GLOSSARIO.md](./GLOSSARIO.md) para termos técnicos e de negócio.

# Research: Fundação do Serviço de Agente

## Orquestração e segurança

**Decision**: Usar um grafo assíncrono com estado tipado e rota determinística de
crise antes de qualquer chamada ao LLM.

**Rationale**: Segurança não pode depender da disponibilidade ou qualidade do
provider. Nodes pequenos tornam roteamento, observabilidade e testes explícitos.

**Alternatives considered**: Um único prompt para classificar e responder foi
rejeitado por misturar responsabilidades e falhar de modo inseguro.

## Limite de autoridade das tools

**Decision**: Executar somente tools de consulta. Confirmação e cancelamento são
ações propostas, validadas e devolvidas à aplicação interna.

**Rationale**: A clarificação da feature reserva validação, autorização e
execução à aplicação interna, preservando integridade transacional.

**Alternatives considered**: Chamar endpoints mutáveis pelo agente foi rejeitado
por ampliar autoridade e exigir idempotência/conciliação dentro do agente.

## Provider LLM

**Decision**: Definir `LLMProvider` no domínio e implementar somente Composer
2.5 via HTTP. Testes usam stubs privados da suíte.

**Rationale**: Evita dependência de SDK específico, mantém testes offline e
isola detalhes de autenticação, timeout e parsing sem oferecer outro modelo em
runtime.

**Alternatives considered**: SDK de fornecedor no domínio foi rejeitado por
acoplamento; providers simulados ou fallback para outro modelo foram rejeitados
para manter o Composer como único modelo suportado em runtime.

## Contexto temporário

**Decision**: Armazenar resumo mínimo por sessão em Redis com TTL configurável,
padrão de 30 minutos, renovado em interações válidas.

**Rationale**: Mantém continuidade sem criar histórico permanente ou fonte de
verdade. A indisponibilidade de Redis degrada a conversa, mas não bloqueia uma
resposta segura.

**Alternatives considered**: Retenção de 24 horas aumenta exposição; expiração
após cada resposta elimina continuidade; persistência durável é fora de escopo.

## Contratos e validação

**Decision**: Usar modelos Pydantic estritos, enums conhecidos, `extra=forbid`,
versão de contrato e validação em todas as fronteiras.

**Rationale**: Bloqueia campos inesperados e ações inventadas, além de tornar
falhas reproduzíveis em testes de contrato.

**Alternatives considered**: Dicionários livres foram rejeitados por permitirem
propagação de conteúdo inválido ou sensível.

## Falhas e prontidão

**Decision**: Timeouts de LLM e tools são configuráveis; falhas retornam
mensagem segura e handoff quando necessário. Readiness depende de configuração
e Redis, não de LLM ou aplicação interna.

**Rationale**: Dependências externas podem oscilar sem exigir retirada imediata
da instância, desde que ela consiga produzir resposta segura.

**Alternatives considered**: Marcar a instância não pronta por qualquer falha
externa poderia causar indisponibilidade total durante degradações transitórias.

## Privacidade e observabilidade

**Decision**: Logs JSON com allowlist de campos, `request_id`, hash de sessão,
node, intenção, duração, resultado externo e motivo codificado.

**Rationale**: Permite diagnóstico e correlação sem registrar mensagens,
prompts, tokens ou dados pessoais.

**Alternatives considered**: Redação por busca textual foi rejeitada como
controle principal; allowlist reduz o risco de vazamento por novos campos.

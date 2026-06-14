# Architecture Decisions

## Escopo e autoridade

O Agent é um serviço stateless de processamento e orquestração de LLM. A
aplicação interna envia o contexto necessário em cada request e continua
responsável por estado, regras de negócio, consultas autoritativas, pagamentos e
execução de ações.

O Agent nunca acessa PostgreSQL ou APIs internas diretamente. Confirmação e
cancelamento são apenas ações estruturadas propostas para validação e execução
pela aplicação interna.

## KISS e SOLID

- O `Orchestrator` compila e executa um LangGraph pequeno, com estado tipado,
  nodes coesos e roteamento condicional explícito.
- Os nodes permanecem juntos em `orchestrator.py` enquanto o fluxo for pequeno;
  eles serão extraídos apenas quando novas features justificarem a separação.
- `LLMProvider` mantém a inversão de dependência, mas o Composer é a única
  implementação de produção. Testes usam stubs privados por injeção.
- Contratos, segurança, ações e logs ficam em módulos pequenos e focados.
- Redis e clientes REST foram removidos porque duplicavam responsabilidades da
  aplicação interna.

## Segurança e privacidade

A detecção determinística de crise roda antes do prompt e da chamada LLM.
Sinais inequívocos interrompem o fluxo e geram escalonamento humano; risco
ambíguo interrompe o processamento administrativo e solicita confirmação.

Modelos rejeitam campos inesperados. Prompts usam contexto mínimo permitido.
Logs são construídos por allowlist e nunca recebem mensagem completa, prompt,
tokens, CPF, pagamento ou conteúdo clínico.

## Falhas e observabilidade

Falha, timeout ou resposta inválida do provider resultam em resposta segura e
handoff humano. Eventos estruturados contêm apenas request ID, sessão
anonimizada, etapa, intenção, duração, resultado externo e motivos codificados.

## Alternativas rejeitadas

- Redis no Agent: o estado já pertence à aplicação interna.
- Um package e arquivo por node desde a fundação: aumenta a navegação antes de
  existir complexidade que justifique essa fragmentação.
- Clientes REST internos no Agent: criam uma segunda camada de orquestração.
- Acesso direto ao PostgreSQL: viola propriedade e privacidade.
- Segurança delegada apenas ao LLM: falha quando o provider está indisponível.


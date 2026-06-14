# AutoCare Agent

Serviço Python/FastAPI responsável somente pelo processamento seguro e pela
orquestração de conversas com LLM. Ele fica atrás da aplicação interna, que
continua sendo a autoridade sobre estado, preços, descontos, disponibilidade,
agendamentos, pagamentos e demais regras de negócio.

## Responsabilidade do serviço

O Agent:

- recebe mensagens e contexto mínimo via `POST /agent/process`;
- detecta crise antes de chamar o LLM;
- classifica a intenção da conversa;
- chama um provider LLM desacoplado;
- valida ações estruturadas propostas;
- retorna handoff humano quando não pode responder com segurança;
- produz logs estruturados e sanitizados.

O Agent não:

- acessa PostgreSQL ou outro banco;
- persiste sessão;
- chama APIs da aplicação interna;
- processa pagamentos;
- executa ações críticas;
- inventa preços, descontos, disponibilidade ou confirmações;
- fornece diagnóstico médico.

```text
Paciente -> Aplicação interna -> AutoCare Agent -> Aplicação interna -> Paciente
                estado/regras      LLM/safety       valida/executa
```

## Arquitetura simplificada

O serviço é stateless: todo contexto necessário deve ser enviado pela aplicação
interna em cada request.

```text
src/autocare_agent/
├── app.py           # FastAPI, rotas, autenticação e composição
├── config.py        # Variáveis de ambiente
├── schemas.py       # Contratos Pydantic de entrada e saída
├── orchestrator.py  # Estado, nodes e fluxo LangGraph
├── llm.py           # Contrato LLMProvider e implementação Composer
├── safety.py        # Crise e handoff
├── actions.py       # Validação de ações estruturadas
└── logging.py       # Logs sanitizados
```

O desenho mantém SOLID onde ele agrega valor:

- `LLMProvider` aplica inversão de dependência e permite trocar providers;
- cada módulo possui uma responsabilidade clara;
- FastAPI depende do `Orchestrator`, não de detalhes do Composer;
- LangGraph fornece o ponto de extensão para os próximos fluxos sem espalhar
  nodes em dezenas de arquivos;
- não existem abstrações para Redis ou tools que o serviço não usa.

Consulte também:

- [Guia didático da arquitetura Python](./docs/guia-arquitetura-python.md)
- [Decisões arquiteturais](./docs/architecture-decisions.md)
- [Stack e integração](./wiki/STACK_REAL.md)
- [Arquitetura ampla do produto](./wiki/ARQUITETURA.md)
- [Fluxos principais](./wiki/FLUXOS_PRINCIPAIS.md)
- [Regras de negócio](./wiki/REGRAS_NEGOCIO.md)
- [Glossário](./wiki/GLOSSARIO.md)

## Fluxo do endpoint principal

```text
POST /agent/process
  -> autenticar e gerar/propagar request_id
  -> invocar LangGraph
     -> sanitize_input
     -> safety
     -> classify_intent
     -> conversation
     -> validate_actions
     -> build_response
  -> registrar log sanitizado
```

Crise, risco ambíguo e pedido explícito de humano interrompem o fluxo antes do
LLM. Falhas do provider retornam resposta segura com handoff.

## Stack

- Python 3.12
- FastAPI e Uvicorn
- LangGraph
- Pydantic v2 e pydantic-settings
- HTTPX assíncrono
- pytest, pytest-asyncio e respx
- Ruff e mypy
- Docker e Docker Compose

O `ComposerLLMProvider` é a única implementação de produção. A abstração
`LLMProvider` permanece para desacoplar o fluxo e permitir stubs privados nos
testes, sem oferecer outro modelo em runtime.

## Executando localmente

### Início rápido no Windows

Depois de preencher `COMPOSER_API_KEY` no arquivo `.env`, execute somente:

```powershell
.\start.cmd
```

O comando:

- cria `.env` quando necessário;
- cria `.venv` com Python 3.12 quando necessário;
- instala dependências quando necessário;
- valida a configuração;
- inicia a API e o Swagger.

Não é necessário ativar manualmente a `.venv` ou executar o comando do Uvicorn.

Para apenas validar a configuração:

```powershell
.\start.cmd -CheckOnly
```

### Pré-requisitos

- Python 3.12
- Git
- Docker Desktop apenas para a opção com container

### Configuração inicial

Na primeira execução, caso a chave ainda não esteja configurada, o comando
criará `.env` e solicitará o preenchimento:

```powershell
.\start.cmd
notepad .env
```

Configure:

```env
COMPOSER_API_KEY=seu-segredo
```

Depois, inicie:

```powershell
.\start.cmd
```

### Docker Compose

```powershell
docker compose up --build
```

O Compose inicia somente a aplicação, pois o Agent não persiste estado.

Para executar em segundo plano e acompanhar logs:

```powershell
docker compose up --build -d
docker compose logs -f app
```

Para encerrar:

```powershell
docker compose down
```

## Swagger e health checks

Com a API iniciada:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Liveness: `http://localhost:8000/health/live`
- Readiness: `http://localhost:8000/health/ready`

```powershell
Invoke-RestMethod http://localhost:8000/health/live
Invoke-RestMethod http://localhost:8000/health/ready
```

Para testar `/agent/process` pelo Swagger:

1. abra `http://localhost:8000/docs`;
2. clique em **Authorize**;
3. informe somente o valor de `APP_AUTH_TOKEN`, sem escrever `Bearer`;
4. clique em **Authorize** novamente e execute o endpoint.

O Swagger adiciona automaticamente `Authorization: Bearer <token>` e preserva
o token durante a sessão do navegador.

## Exemplo de request

```powershell
$headers = @{
  Authorization = "Bearer local-development-token"
  "X-Request-ID" = "018f4d12-3b3d-7cc0-a891-c52f388bc001"
}

$body = @{
  contract_version = "1.0"
  paciente_id = "018f4d12-3b3d-7cc0-a891-c52f388bc002"
  sessao_id = "018f4d12-3b3d-7cc0-a891-c52f388bc003"
  mensagem = "Quero conhecer os horários disponíveis."
  contexto = @{
    locale = "pt-BR"
    timezone = "America/Sao_Paulo"
    resumo_sessao = "Paciente deseja informações administrativas."
  }
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/agent/process `
  -Headers $headers `
  -ContentType "application/json" `
  -Body $body
```

## Configuração do Composer

O Composer 2.5 é o único provider suportado:

```env
COMPOSER_BASE_URL=https://api-for-cursor.standardagents.ai/opencode/v1
COMPOSER_API_KEY=seu-segredo
COMPOSER_MODEL=composer-2.5
COMPOSER_TIMEOUT_SECONDS=10
```

Nunca versione `.env` com segredos.

O host `cursor-api.standardagents.ai` não deve ser usado como base: ele
redireciona para outro domínio e o HTTPX remove corretamente o header de
autorização durante redirects entre hosts.

Em teste realizado com `composer-2.5`, o endpoint confirmou que o modelo está
disponível, mas a execução de chat retornou que Cloud Agent exige uma conta Pro.
Nesse cenário, o Agent retorna `falha_segura` e solicita handoff humano.

## Testes e qualidade

```powershell
pytest -q
ruff check src tests
ruff format --check src tests
mypy src
```

Os testes usam stubs privados e mocks HTTP; eles não precisam de rede real nem
oferecem um provider alternativo para execução da aplicação.

## VS Code

Extensões recomendadas:

- Python, da Microsoft;
- Pylance, da Microsoft;
- Ruff, da Astral Software;
- Docker, da Microsoft;
- REST Client, opcional para testar endpoints.

Selecione o interpretador em `.venv` e use esta configuração de debug:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "AutoCare Agent API",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["autocare_agent.app:app", "--reload", "--port", "8000"],
      "envFile": "${workspaceFolder}/.env",
      "justMyCode": true
    }
  ]
}
```

## Problemas comuns

- `401 unauthorized`: confira se `Authorization: Bearer ...` usa
  `APP_AUTH_TOKEN`.
- `COMPOSER_API_KEY is required`: abra `.env` e preencha
  `COMPOSER_API_KEY`. Copiar `.env.example` cria intencionalmente uma chave
  vazia.
- Porta 8000 ocupada: encerre o processo existente ou use outra porta.
- Composer indisponível: o Agent retorna `falha_segura`; não existe fallback
  para outro modelo.
- Composer retorna `Cloud Agent is not available for free users`: a API key e o
  modelo foram reconhecidos, mas a conta precisa de plano Pro.
- Import não encontrado: ative `.venv` e execute `python -m pip install -e
  ".[dev]"`.

## Limites atuais

- A detecção de crise e a classificação inicial usam termos determinísticos e
  devem evoluir com critérios aprovados.
- A integração Composer precisa ser validada contra o endpoint real.
- A aplicação interna deve correlacionar `action_id`, autorizar e executar toda
  ação proposta.

**Versão:** 1.0
**Data:** Junho de 2026

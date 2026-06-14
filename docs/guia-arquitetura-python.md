# Guia Didático da Arquitetura Python

Este guia explica o AutoCare Agent para quem ainda não conhece Python,
FastAPI, Pydantic ou a organização do projeto.

## 1. Modelo mental

O Agent é uma API pequena e stateless. Ele recebe uma mensagem da aplicação
interna, aplica regras de segurança, chama o LLM e devolve uma resposta
estruturada.

```text
Aplicação interna
    |
    | POST /agent/process + contexto mínimo
    v
FastAPI -> Orchestrator/LangGraph -> Safety -> LLMProvider -> validação de ações
    |
    v
ProcessResponse
```

Stateless significa que o Agent não guarda a conversa. A aplicação interna
envia em `contexto.resumo_sessao` apenas o resumo necessário para aquele
request.

## 2. Conceitos Python usados

| Conceito no projeto | Equivalente aproximado |
|---|---|
| arquivo `.py` | módulo/classe em outras stacks |
| `pyproject.toml` | `.csproj`, `pom.xml` ou `package.json` |
| `.venv` | ambiente isolado de dependências |
| Pydantic `BaseModel` | DTO com validação automática |
| `Protocol` | interface estrutural |
| `str \| None` | string opcional |
| `async def` / `await` | método assíncrono / Task / Promise |
| `pytest` | framework de testes |
| Ruff | linter e formatador |
| mypy | verificador estático de tipos |

### Imports

```python
from autocare_agent.schemas import ProcessRequest
```

Isso importa `ProcessRequest` do arquivo:

```text
src/autocare_agent/schemas.py
```

### Tipos

```python
async def process(
    request: ProcessRequest,
    request_id: UUID,
) -> ProcessResponse:
```

O método recebe um request validado e um UUID, é assíncrono e retorna um
`ProcessResponse`. O mypy verifica esses contratos sem executar a aplicação.

### Pydantic

Pydantic converte JSON em objetos Python e valida tipos e regras.

```python
class ProcessRequest(StrictModel):
    paciente_id: UUID
    sessao_id: UUID
    mensagem: str
```

UUID inválido, campo ausente ou campo extra resultam em HTTP `422`. Os modelos
herdam de `StrictModel`, que rejeita campos não declarados. Assim, um `cpf`
enviado acidentalmente dentro de `contexto` não chega ao fluxo.

## 3. Estrutura

```text
src/autocare_agent/
├── app.py
├── config.py
├── schemas.py
├── orchestrator.py
├── llm.py
├── safety.py
├── actions.py
└── logging.py
```

### `app.py`

É a borda HTTP e o ponto de entrada da aplicação. Contém:

- criação do FastAPI;
- autenticação bearer;
- geração e propagação de `request_id`;
- rotas `/agent/process`, `/health/live` e `/health/ready`;
- seleção do provider LLM;
- Swagger gerado automaticamente.

O comando:

```powershell
.\start.cmd
```

cria ou reutiliza a `.venv`, valida a configuração e inicia o Uvicorn com o
objeto `app` do módulo `autocare_agent.app`.

### `config.py`

Lê variáveis de ambiente com `pydantic-settings`. Segredos usam `SecretStr`
para não aparecerem acidentalmente em logs ou no debugger.

### `schemas.py`

Define os contratos que entram, saem e circulam entre os módulos:

| Modelo | Responsabilidade |
|---|---|
| `ProcessRequest` | request de `/agent/process` |
| `ConversationContext` | contexto mínimo permitido |
| `ProcessResponse` | resposta final |
| `LLMResult` | resposta aceita do provider |
| `ProposedAction` | ação que a aplicação interna deve validar |
| `CrisisAlert` | alerta estruturado de crise |
| `HandoffDossier` | dados mínimos para transferência humana |

### `orchestrator.py`

É o caso de uso principal. O `Orchestrator` compila um LangGraph pequeno com
estado tipado (`AgentState`) e os seguintes nodes:

```text
START
  -> sanitize_input
  -> safety
     -> crise/humano/resultado autoritativo -> build_response
     -> normal -> classify_intent -> conversation -> validate_actions
  -> build_response
  -> END
```

Os nodes permanecem no mesmo arquivo enquanto o fluxo for pequeno. Isso mantém
o uso do LangGraph para as próximas features sem criar antecipadamente uma
pasta e um arquivo para cada etapa.

O grafo é compilado uma vez quando o `Orchestrator` é criado e executado com
`graph.ainvoke(...)` em cada request.

### `llm.py`

Contém a única interface de infraestrutura do núcleo:

```python
class LLMProvider(Protocol):
    async def generate(...) -> LLMResult: ...
```

Qualquer provider que implemente esse método pode ser injetado no
`Orchestrator`.

- `ComposerLLMProvider`: única implementação de produção, chama o Composer 2.5
  usando HTTPX;
- stubs definidos somente em `tests/`: isolam testes sem criar outro provider
  configurável;
- `build_system_prompt`: envia somente contexto permitido.

### `safety.py`

Executa antes do LLM:

- identifica sinais explícitos de crise;
- bloqueia o fluxo normal em risco ambíguo;
- reconhece pedido explícito de atendimento humano;
- cria orientação e dossiê sanitizado.

### `actions.py`

Valida ações sugeridas pelo modelo. Confirmação e cancelamento exigem parâmetros
tipados e permanecem no modo `propose`. O Agent nunca executa essas ações.

Também bloqueia uma ação quando o `request_id` retornado não corresponde ao
request atual.

### `logging.py`

Cria logs por allowlist. Mesmo que alguém tente registrar `mensagem`, `cpf` ou
outro campo sensível, esses valores são descartados.

## 4. Fluxo completo de um request

### 4.1 Middleware

Antes da rota, `SecurityMiddleware`:

1. lê `X-Request-ID` ou gera um UUID;
2. exige bearer token em `/agent/*`;
3. guarda o ID em `request.state.request_id`;
4. devolve o mesmo ID no header da resposta.

Health checks e Swagger permanecem públicos.

### 4.2 Validação

FastAPI transforma o JSON em `ProcessRequest`. Pydantic rejeita dados inválidos
antes de executar o `Orchestrator`.

### 4.3 Injeção de dependência

`get_orchestrator()` sempre monta o Composer:

```text
Settings -> ComposerLLMProvider -> Orchestrator
```

`@lru_cache` reutiliza a instância durante a vida do processo.

### 4.4 Segurança

Crise e risco ambíguo interrompem imediatamente o processamento. O provider LLM
não é chamado nesses caminhos.

### 4.5 LLM e falha segura

Para uma mensagem normal:

1. a intenção inicial é classificada;
2. um prompt mínimo é construído;
3. o provider retorna `LLMResult`;
4. ações são validadas;
5. o Agent retorna `ProcessResponse`.

Qualquer exceção do provider gera resposta segura e `dossie_handoff`.

## 5. Por que a arquitetura foi simplificada

A aplicação interna já controla sessão, regras, estado e integrações. Manter
Redis, clientes REST e uma máquina de estados no Agent criava duas camadas de
orquestração.

A versão atual aplica KISS:

- menos módulos para navegar;
- LangGraph concentrado em um único caso de uso;
- nodes visíveis em um único arquivo enquanto ainda são pequenos;
- testes focados em comportamento;
- nenhuma duplicação de estado.

E mantém SOLID:

- responsabilidade única por módulo;
- provider LLM substituível;
- núcleo depende de `LLMProvider`, não do Composer;
- contratos explícitos separam FastAPI, orquestração e integração.

## 6. Autoridade e segurança

A aplicação interna é responsável por:

- persistência e histórico;
- preços, descontos e disponibilidade;
- autorização e regras de negócio;
- correlação e execução de ações;
- pagamentos e notificações.

O Agent pode propor ações estruturadas, mas nunca deve informar sucesso baseado
apenas no modelo. Uma confirmação só é exibida quando o request contém
`contexto.resultado_autoritativo` com status `success` e protocolo válido.

## 7. Swagger

FastAPI gera documentação a partir das rotas e dos modelos Pydantic:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
- `http://localhost:8000/openapi.json`

Use o Swagger para explorar formatos. O endpoint `/agent/process` exige:

```text
Authorization: Bearer local-development-token
```

No `/docs`, clique em **Authorize** e informe somente o token configurado em
`APP_AUTH_TOKEN`. O Swagger adiciona o prefixo `Bearer` automaticamente e
mantém o token durante a sessão do navegador.

## 8. Testes

Os testes estão em `tests/` e usam nomes próximos aos módulos:

```text
tests/
├── conftest.py
├── test_api.py
├── test_orchestrator.py
├── test_llm.py
├── test_actions.py
├── test_schemas.py
├── test_logging.py
└── test_config.py
```

`conftest.py` cria fixtures reutilizáveis, como cliente FastAPI, autenticação e
payload padrão.

```powershell
pytest -q
pytest tests/test_orchestrator.py -q
pytest tests/test_api.py::test_normal_request -q
```

## 9. Como depurar

Coloque breakpoints nesta ordem:

1. `app.py`, em `SecurityMiddleware.dispatch`;
2. `app.py`, em `process_agent`;
3. `orchestrator.py`, em `Orchestrator.process`;
4. `orchestrator.py`, nos nodes `_safety`, `_conversation` e `_build_response`;
5. `safety.py`, em `detect_crisis`;
6. `llm.py`, em `generate`;
7. `actions.py`, em `validate_actions`.

Configuração sugerida para `.vscode/launch.json`:

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

## 10. Alterações comuns

### Adicionar intenção

1. adicione o valor em `schemas.py`;
2. ajuste `classify_intent()` em `orchestrator.py`;
3. ajuste o stub privado dos testes, se necessário;
4. adicione teste.

### Adicionar provider

1. implemente `LLMProvider.generate`;
2. valide a resposta como `LLMResult`;
3. selecione o provider em `get_orchestrator()`;
4. teste sucesso, timeout e resposta inválida.

### Adicionar ação

1. adicione o tipo em `ActionType`;
2. defina os parâmetros em `actions.py`;
3. valide a ação em `validate_actions`;
4. documente como a aplicação interna deve executá-la;
5. adicione testes.

### Adicionar endpoint

Para poucos endpoints, adicione a rota em `app.py`. Quando esse arquivo começar
a concentrar muitos contextos diferentes, extraia routers por área. Não crie
camadas antecipadamente.

## 11. Ordem recomendada de leitura

1. `schemas.py`: descubra o contrato;
2. `orchestrator.py`: entenda o fluxo;
3. `app.py`: veja a borda HTTP e a composição;
4. `safety.py`: entenda interrupções seguras;
5. `llm.py`: veja providers e prompt;
6. `actions.py`: entenda limites de autoridade;
7. `tests/test_orchestrator.py`: veja exemplos executáveis.

Resumo mental:

> FastAPI recebe e valida; Orchestrator executa o LangGraph; Safety interrompe
> riscos; LLMProvider conversa; Actions bloqueia propostas inválidas; a
> aplicação interna continua sendo a autoridade.

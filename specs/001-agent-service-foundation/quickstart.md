# Quickstart: Fundação do Serviço de Agente

## Pré-requisitos

- Python 3.12
- Docker e Docker Compose

## Configuração local

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Para execução local sem chamadas LLM externas, configure:

```env
LLM_PROVIDER=fake
```

## Verificação

```powershell
Invoke-RestMethod http://localhost:8000/health/live
Invoke-RestMethod http://localhost:8000/health/ready
pytest
ruff check .
ruff format --check .
mypy src
```

## Exemplo de processamento

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
  }
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/agent/process `
  -Headers $headers `
  -ContentType "application/json" `
  -Body $body
```

O ambiente de testes não deve exigir rede real. `FakeLLMProvider`, sessão em
memória e mocks `respx` substituem as dependências externas.

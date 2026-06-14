# Quickstart: Fundação do Serviço de Agente

## Pré-requisitos

- Python 3.12
- Docker e Docker Compose

## Configuração local

```powershell
.\start.cmd
```

Na primeira execução, o comando cria `.env`. Preencha a credencial solicitada:

```env
COMPOSER_API_KEY=seu-segredo
```

Depois execute `.\start.cmd` novamente. O script cria a `.venv`, instala
dependências quando necessário, valida a configuração e inicia a API.

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

O ambiente de testes não exige rede real. Stubs privados da suíte e mocks
`respx` substituem a chamada ao Composer sem oferecer outro provider em runtime.

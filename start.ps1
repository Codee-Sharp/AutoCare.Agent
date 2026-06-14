param(
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Arquivo .env criado."
}

$configuredKey = Get-Content ".env" |
    Where-Object { $_ -match "^COMPOSER_API_KEY=" } |
    Select-Object -First 1
$fileKey = if ($configuredKey) { $configuredKey.Substring("COMPOSER_API_KEY=".Length).Trim() } else { "" }

if ([string]::IsNullOrWhiteSpace($env:COMPOSER_API_KEY) -and [string]::IsNullOrWhiteSpace($fileKey)) {
    Write-Host ""
    Write-Host "Configure COMPOSER_API_KEY no arquivo .env e execute .\start.cmd novamente." -ForegroundColor Yellow
    exit 1
}

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Criando ambiente virtual..."
    if (Get-Command "py" -ErrorAction SilentlyContinue) {
        py -3.12 -m venv .venv
    }
    elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
        python -m venv .venv
    }
    else {
        Write-Host "Python 3.12 nao foi encontrado." -ForegroundColor Red
        exit 1
    }
}

& $venvPython -c "import uvicorn, autocare_agent" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Instalando dependencias..."
    & $venvPython -m pip install -e ".[dev]"
}

& $venvPython -c "from autocare_agent.config import Settings; Settings(); print('Configuracao valida.')"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if ($CheckOnly) {
    exit 0
}

Write-Host "Iniciando AutoCare Agent em http://localhost:8000"
Write-Host "Swagger: http://localhost:8000/docs"
& $venvPython -m uvicorn autocare_agent.app:app --reload --host 0.0.0.0 --port 8000

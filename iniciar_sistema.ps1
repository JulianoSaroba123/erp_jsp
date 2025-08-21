# JSP ELÉTRICA ERP - Inicializador PowerShell
# Script moderno para Windows PowerShell

param(
    [switch]$NoGui,
    [switch]$Help
)

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ██╗███████╗██████╗     ███████╗██╗     ███████╗████████╗██████╗ ██╗ ██████╗ █████╗ " -ForegroundColor Cyan
    Write-Host "  ██║██╔════╝██╔══██╗    ██╔════╝██║     ██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝██╔══██╗" -ForegroundColor Cyan
    Write-Host "  ██║███████╗██████╔╝    █████╗  ██║     █████╗     ██║   ██████╔╝██║██║     ███████║" -ForegroundColor Cyan
    Write-Host "  ██║╚════██║██╔═══╝     ██╔══╝  ██║     ██╔══╝     ██║   ██╔══██╗██║██║     ██╔══██║" -ForegroundColor Cyan
    Write-Host "  ██║███████║██║         ███████╗███████╗███████╗   ██║   ██║  ██║██║╚██████╗██║  ██║" -ForegroundColor Cyan
    Write-Host "  ╚═╝╚══════╝╚═╝         ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "                         Sistema ERP - Gestão de Ordens de Serviço" -ForegroundColor White
    Write-Host "=" * 80 -ForegroundColor Gray
}

function Test-Environment {
    Write-Host "[INFO] Verificando ambiente..." -ForegroundColor Yellow
    
    # Verificar se está no diretório correto
    if (-not (Test-Path "run.py")) {
        Write-Host "[ERRO] Arquivo run.py não encontrado!" -ForegroundColor Red
        Write-Host "       Execute este script no diretório do projeto." -ForegroundColor Red
        return $false
    }
    
    # Verificar ambiente virtual
    if (-not (Test-Path ".venv")) {
        Write-Host "[ERRO] Ambiente virtual não encontrado!" -ForegroundColor Red
        Write-Host "       Execute: python -m venv .venv" -ForegroundColor Red
        return $false
    }
    
    # Verificar Python no venv
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        Write-Host "[ERRO] Python do ambiente virtual não encontrado!" -ForegroundColor Red
        return $false
    }
    
    Write-Host "[OK] Ambiente verificado!" -ForegroundColor Green
    return $true
}

function Start-FlaskServer {
    Write-Host "[INFO] Iniciando servidor Flask..." -ForegroundColor Yellow
    Write-Host "=" * 80 -ForegroundColor Gray
    Write-Host "  🚀 SERVIDOR INICIANDO..." -ForegroundColor Green
    Write-Host "  "
    Write-Host "  🌐 URL do Sistema: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "  "
    Write-Host "  ⏳ Aguarde alguns segundos..." -ForegroundColor Yellow
    Write-Host "  🌍 O navegador abrirá automaticamente" -ForegroundColor Yellow
    Write-Host "  ⛔ Para parar o servidor: Pressione Ctrl+C" -ForegroundColor Red
    Write-Host "=" * 80 -ForegroundColor Gray
    Write-Host ""
    
    # Configurar variáveis de ambiente
    $env:FLASK_APP = "run.py"
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    
    # Abrir navegador em background após 3 segundos
    if (-not $NoGui) {
        Start-Job -ScriptBlock {
            Start-Sleep 3
            Start-Process "http://localhost:5000"
        } | Out-Null
    }
    
    try {
        # Ativar ambiente virtual e iniciar Flask
        & ".\.venv\Scripts\python.exe" "run.py"
    }
    catch {
        Write-Host "[ERRO] Falha ao iniciar servidor: $_" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Show-Help {
    Write-Host "JSP ELÉTRICA ERP - Sistema de Gestão" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso:" -ForegroundColor White
    Write-Host "  .\iniciar_sistema.ps1                 # Iniciar com interface gráfica"
    Write-Host "  .\iniciar_sistema.ps1 -NoGui          # Iniciar sem abrir navegador"
    Write-Host "  .\iniciar_sistema.ps1 -Help           # Mostrar esta ajuda"
    Write-Host ""
    Write-Host "Exemplos:" -ForegroundColor White
    Write-Host "  .\iniciar_sistema.ps1                 # Modo padrão (recomendado)"
    Write-Host "  .\iniciar_sistema.ps1 -NoGui          # Para servidores/automação"
    Write-Host ""
}

# Função principal
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    Show-Banner
    
    if (-not (Test-Environment)) {
        Write-Host ""
        Read-Host "Pressione Enter para sair"
        return
    }
    
    if (-not (Start-FlaskServer)) {
        Write-Host ""
        Read-Host "Pressione Enter para sair"
        return
    }
    
    Write-Host ""
    Write-Host "[INFO] Sistema encerrado." -ForegroundColor Green
}

# Executar função principal
Main

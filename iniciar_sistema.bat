@echo off
title JSP ELETRICA - ERP System
color 0A

echo.
echo  ██╗███████╗██████╗     ███████╗██╗     ███████╗████████╗██████╗ ██╗ ██████╗ █████╗ 
echo  ██║██╔════╝██╔══██╗    ██╔════╝██║     ██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝██╔══██╗
echo  ██║███████╗██████╔╝    █████╗  ██║     █████╗     ██║   ██████╔╝██║██║     ███████║
echo  ██║╚════██║██╔═══╝     ██╔══╝  ██║     ██╔══╝     ██║   ██╔══██╗██║██║     ██╔══██║
echo  ██║███████║██║         ███████╗███████╗███████╗   ██║   ██║  ██║██║╚██████╗██║  ██║
echo  ╚═╝╚══════╝╚═╝         ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝
echo.
echo                              Sistema ERP - Gestao de Ordens de Servico
echo.
echo ================================================================================

REM Verificar se esta no diretorio correto
if not exist "run.py" (
    echo ERRO: Arquivo run.py nao encontrado!
    echo Certifique-se de que esta no diretorio correto do projeto.
    pause
    exit /b 1
)

REM Verificar se o ambiente virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute 'python -m venv .venv' para criar o ambiente virtual.
    pause
    exit /b 1
)

echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado!

REM Verificar dependencias
echo [INFO] Verificando dependencias...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [AVISO] Flask nao encontrado. Instalando dependencias...
    pip install -r requirements.txt
)

REM Configurar variaveis
set FLASK_APP=run.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo [INFO] Configuracoes:
echo        - Aplicacao: %FLASK_APP%
echo        - Ambiente: %FLASK_ENV%
echo        - Debug: %FLASK_DEBUG%
echo.

echo ================================================================================
echo  SERVIDOR INICIANDO...
echo  
echo  URL do Sistema: http://localhost:5000
echo  
echo  Aguarde alguns segundos e o navegador abrira automaticamente
echo  Para parar o servidor: Pressione Ctrl+C nesta janela
echo ================================================================================
echo.

REM Aguardar 3 segundos e abrir navegador em background
start /b timeout /t 3 /nobreak >nul && start http://localhost:5000

REM Iniciar servidor Flask
python run.py

echo.
echo [INFO] Servidor encerrado.
echo Pressione qualquer tecla para fechar...
pause >nul

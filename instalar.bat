@echo off
title Instalacao JSP ELETRICA ERP
color 0B

echo.
echo  ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗      █████╗  ██████╗ █████╗  ██████╗ 
echo  ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██╔══██╗██╔════╝██╔══██╗██╔═══██╗
echo  ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ███████║██║     ███████║██║   ██║
echo  ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██╔══██║██║     ██╔══██║██║   ██║
echo  ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗██║  ██║╚██████╗██║  ██║╚██████╔╝
echo  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ 
echo.
echo                              JSP ELETRICA - Sistema ERP
echo                                   Instalacao Automatica
echo.
echo ================================================================================

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo        Instale Python 3.8+ de https://python.org
    echo        Certifique-se de marcar "Add to PATH" durante a instalacao
    pause
    exit /b 1
)
echo [OK] Python encontrado!

echo.
echo [2/5] Criando ambiente virtual...
if exist ".venv" (
    echo [INFO] Ambiente virtual ja existe. Removendo...
    rmdir /s /q .venv
)
python -m venv .venv
if errorlevel 1 (
    echo [ERRO] Falha ao criar ambiente virtual!
    pause
    exit /b 1
)
echo [OK] Ambiente virtual criado!

echo.
echo [3/5] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado!

echo.
echo [4/5] Instalando dependencias...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [INFO] Instalando dependencias basicas...
    pip install flask sqlalchemy flask-sqlalchemy python-dotenv
)
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas!

echo.
echo [5/5] Testando instalacao...
python -c "import flask; print('Flask OK')"
if errorlevel 1 (
    echo [ERRO] Falha no teste de instalacao!
    pause
    exit /b 1
)
echo [OK] Instalacao testada com sucesso!

echo.
echo ================================================================================
echo  INSTALACAO CONCLUIDA COM SUCESSO!
echo  
echo  Para executar o sistema:
echo  1. Execute: iniciar_sistema.bat
echo  2. Ou: python iniciar_sistema.py
echo  
echo  O sistema sera aberto automaticamente no navegador
echo  URL: http://localhost:5000
echo ================================================================================
echo.

echo Deseja iniciar o sistema agora? (S/N)
set /p choice=
if /i "%choice%"=="S" (
    echo.
    echo Iniciando sistema...
    call iniciar_sistema.bat
)

echo.
echo Instalacao finalizada. Pressione qualquer tecla para sair...
pause >nul

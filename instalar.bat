@echo off
title JSP ELÉTRICA - Instalador do Sistema
echo.
echo ================================================
echo    JSP ELÉTRICA - Sistema ERP
echo    Instalador Automático
echo ================================================
echo.

echo 🔧 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale o Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo.
echo 📦 Criando ambiente virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar ambiente virtual.
    pause
    exit /b 1
)

echo.
echo 🔌 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo 📚 Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências.
    pause
    exit /b 1
)

echo.
echo ✅ Instalação concluída com sucesso!
echo.
echo Para iniciar o sistema, execute:
echo   iniciar_sistema.bat
echo.
pause

@echo off
title JSP ELÉTRICA - Servidor
echo.
echo ================================================
echo    JSP ELÉTRICA - Sistema ERP
echo    Modo Servidor Simples
echo ================================================
echo.

echo 🔌 Ativando ambiente virtual...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Ambiente virtual não encontrado.
    echo Execute primeiro: instalar.bat
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando servidor Flask...
flask run --host=0.0.0.0 --port=5000 --debug

pause

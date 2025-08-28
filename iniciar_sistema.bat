@echo off
title JSP ELÉTRICA - Sistema ERP
echo.
echo ================================================
echo    JSP ELÉTRICA - Sistema ERP
echo    Inicializando Sistema...
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
echo 🚀 Iniciando sistema...
python iniciar_sistema.py

pause

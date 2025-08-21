@echo off
echo =============================================
echo     GERADOR DE EXECUTAVEL - JSP ELETRICA
echo =============================================
echo.

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar PyInstaller se necessario
echo Verificando PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

REM Criar executavel
echo.
echo Gerando executavel...
echo.

pyinstaller --onefile --windowed --name "JSP_ELETRICA_ERP" --icon=icon.ico iniciar_sistema.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao gerar executavel!
    pause
    exit /b 1
)

echo.
echo =============================================
echo  EXECUTAVEL GERADO COM SUCESSO!
echo  
echo  Localizacao: dist\JSP_ELETRICA_ERP.exe
echo  
echo  Agora voce pode executar o sistema
echo  clicando duas vezes no arquivo .exe
echo =============================================
echo.

REM Copiar executavel para pasta principal
if exist "dist\JSP_ELETRICA_ERP.exe" (
    copy "dist\JSP_ELETRICA_ERP.exe" "JSP_ELETRICA_ERP.exe"
    echo Executavel copiado para a pasta principal!
)

pause

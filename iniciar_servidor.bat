@echo off
echo =============================================
echo           JSP ELETRICA - ERP SYSTEM
echo =============================================
echo.
echo Iniciando servidor Flask...
echo.

REM Navegar para o diretorio do projeto
cd /d "C:\Users\julia\Desktop\Backup ERP\erp_jsp_teste"

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar se a ativacao foi bem-sucedida
if errorlevel 1 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual!
    echo Verifique se o ambiente virtual existe em .venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM Definir variaveis de ambiente
set FLASK_APP=run.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo.
echo Ambiente virtual ativado com sucesso!
echo Iniciando aplicacao Flask...
echo.
echo =============================================
echo  Servidor rodando em: http://localhost:5000
echo  Para parar o servidor: Pressione Ctrl+C
echo =============================================
echo.

REM Iniciar aplicacao Flask
python run.py

REM Se chegou aqui, o servidor foi interrompido
echo.
echo Servidor Flask foi encerrado.
pause

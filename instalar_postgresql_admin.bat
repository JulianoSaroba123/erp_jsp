@echo off
title JSP ELÉTRICA - Instalador PostgreSQL (Administrador)
echo.
echo ================================================
echo    JSP ELÉTRICA - Instalador PostgreSQL
echo    EXECUÇÃO COMO ADMINISTRADOR
echo ================================================
echo.

:: Verificar se está rodando como administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Executando como Administrador
) else (
    echo ❌ Este script precisa ser executado como ADMINISTRADOR
    echo.
    echo 💡 Clique com botão direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

echo.
echo 🔍 Verificando se PostgreSQL está instalado...
psql --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL já está instalado!
    goto :configure
)

echo ❌ PostgreSQL não encontrado.
echo.
echo 📥 Baixando PostgreSQL...

:: Baixar PostgreSQL usando PowerShell
powershell -Command "& {Invoke-WebRequest -Uri 'https://get.enterprisedb.com/postgresql/postgresql-16.1-1-windows-x64.exe' -OutFile 'postgresql_installer.exe'}"

if not exist postgresql_installer.exe (
    echo ❌ Falha no download. Baixe manualmente de:
    echo https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo ✅ Download concluído!
echo.
echo 🔧 Instalando PostgreSQL...
echo ⏳ Isso pode levar alguns minutos...

:: Instalação silenciosa
postgresql_installer.exe --mode unattended --superpassword "123456" --servicename "postgresql" --servicepassword "123456" --serverport "5432" --locale "English, United States" --encoding "UTF8"

if %errorlevel% neq 0 (
    echo ❌ Erro na instalação automática.
    echo 💡 Execute o instalador manualmente: postgresql_installer.exe
    pause
    exit /b 1
)

echo ✅ PostgreSQL instalado com sucesso!
del postgresql_installer.exe

:configure
echo.
echo 🔧 Configurando banco de dados JSP ERP...

:: Adicionar PostgreSQL ao PATH temporariamente
set PATH=%PATH%;C:\Program Files\PostgreSQL\16\bin

echo.
echo 📝 Criando banco e usuário...
(
echo CREATE DATABASE jsp_erp WITH ENCODING = 'UTF8';
echo CREATE USER jsp_user WITH PASSWORD 'jsp123456';
echo ALTER USER jsp_user CREATEDB;
echo GRANT ALL PRIVILEGES ON DATABASE jsp_erp TO jsp_user;
) > setup.sql

echo 🔐 Configurando com senha do postgres: 123456
set PGPASSWORD=123456
psql -U postgres -f setup.sql

if %errorlevel% neq 0 (
    echo ❌ Erro na configuração do banco.
    echo 💡 Tente executar manualmente:
    echo psql -U postgres
    pause
    exit /b 1
)

del setup.sql

echo.
echo 🔄 Atualizando configuração do sistema...
(
echo # Configurações do banco de dados PostgreSQL
echo DATABASE_URL=postgresql://jsp_user:jsp123456@localhost:5432/jsp_erp
echo.
echo # Configurações Flask
echo FLASK_APP=run.py
echo FLASK_ENV=development
echo FLASK_DEBUG=1
echo SECRET_KEY=jsp_eletrica_2025_super_secret_key_dev
echo.
echo # Configurações do sistema
echo COMPANY_NAME=JSP ELÉTRICA
echo SYSTEM_VERSION=1.0
) > .env

echo ✅ Configuração atualizada!
echo.
echo 🎉 PostgreSQL configurado com sucesso!
echo.
echo 📋 Dados da configuração:
echo    Host: localhost
echo    Porta: 5432
echo    Banco: jsp_erp
echo    Usuário: jsp_user
echo    Senha: jsp123456
echo.
echo 🚀 Para iniciar o sistema:
echo    iniciar_sistema.bat
echo.
pause

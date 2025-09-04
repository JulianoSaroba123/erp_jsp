#!/bin/bash
# apt.sh - Script para instalar dependências do sistema necessárias para o WeasyPrint

echo "Instalando dependências do sistema para WeasyPrint..."
apt-get update -y
apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

echo "Instalando dependências adicionais..."
apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi

echo "Dependências do sistema instaladas com sucesso!"

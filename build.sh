#!/usr/bin/env bash
# Build script for Render

# Install system dependencies for WeasyPrint
echo "Instalando dependências do sistema..."
apt-get update -y
apt-get install -y --no-install-recommends libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Install Python dependencies
echo "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo "Executando migrações do banco de dados..."
alembic upgrade head

echo "Build completed successfully!"

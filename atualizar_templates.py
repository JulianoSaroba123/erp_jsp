import os
import shutil
from datetime import datetime

# Diretório dos templates
templates_dir = "app/templates"

# Obter a data atual para o backup
data_atual = datetime.now().strftime("%Y%m%d_%H%M")

# Criar diretório de backup se não existir
backup_dir = f"{templates_dir}/backup_{data_atual}"
os.makedirs(backup_dir, exist_ok=True)

# Lista de arquivos a serem atualizados
arquivos = ["base.html", "index.html"]

# Fazer backup e substituir arquivos
for arquivo in arquivos:
    caminho_original = os.path.join(templates_dir, arquivo)
    caminho_backup = os.path.join(backup_dir, arquivo)
    caminho_novo = os.path.join(templates_dir, f"{arquivo.split('.')[0]}_new.html")
    
    # Verificar se os arquivos existem
    if os.path.exists(caminho_original) and os.path.exists(caminho_novo):
        # Fazer backup do original
        shutil.copy2(caminho_original, caminho_backup)
        print(f"Backup de {arquivo} criado em {caminho_backup}")
        
        # Copiar o novo para substituir o original
        shutil.copy2(caminho_novo, caminho_original)
        print(f"{arquivo} substituído com sucesso")
    else:
        if not os.path.exists(caminho_original):
            print(f"Arquivo original {caminho_original} não encontrado")
        if not os.path.exists(caminho_novo):
            print(f"Novo arquivo {caminho_novo} não encontrado")

print("\nAtualização concluída. Arquivos originais foram copiados para:", backup_dir)

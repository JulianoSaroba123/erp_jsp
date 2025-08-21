#!/usr/bin/env python3
"""
Script para corrigir definitivamente o problema de duplicação
"""

def fix_duplication_definitively():
    file_path = r'c:\Users\julia\Desktop\Backup ERP\erp_jsp_teste\app\ordem_servico\os_routes.py'
    
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dividir por linhas
    lines = content.split('\n')
    print(f"Total de linhas: {len(lines)}")
    
    # Encontrar onde está a função de upload de arquivo (que deve ser uma das últimas)
    cut_point = None
    for i, line in enumerate(lines):
        if 'def upload_arquivo' in line and cut_point is None:
            cut_point = i
            print(f"Primeira ocorrência de upload_arquivo na linha {i+1}")
            
            # Procurar o final desta função
            for j in range(i+1, len(lines)):
                if (lines[j].strip() == '' and 
                    j+1 < len(lines) and 
                    (lines[j+1].startswith('@') or lines[j+1].startswith('def ') or lines[j+1].startswith('from '))):
                    cut_point = j + 1
                    print(f"Final da função upload_arquivo na linha {cut_point}")
                    break
            break
    
    if cut_point is None:
        # Se não encontrou upload_arquivo, vamos procurar por alterar_status
        for i, line in enumerate(lines):
            if 'def alterar_status' in line:
                cut_point = i
                print(f"Primeira ocorrência de alterar_status na linha {i+1}")
                
                # Procurar o final desta função
                for j in range(i+1, len(lines)):
                    if (lines[j].strip() == '' and 
                        j+1 < len(lines) and 
                        (lines[j+1].startswith('@') or lines[j+1].startswith('def ') or lines[j+1].startswith('from '))):
                        cut_point = j + 1
                        print(f"Final da função alterar_status na linha {cut_point}")
                        break
                break
    
    if cut_point is None:
        print("Não consegui encontrar um ponto de corte seguro")
        return
    
    # Cortar o arquivo no ponto encontrado
    clean_lines = lines[:cut_point]
    
    # Remover linhas vazias no final
    while clean_lines and clean_lines[-1].strip() == '':
        clean_lines.pop()
    
    # Salvar arquivo corrigido
    clean_content = '\n'.join(clean_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"Arquivo corrigido!")
    print(f"Linhas originais: {len(lines)}")
    print(f"Linhas finais: {len(clean_lines)}")
    print(f"Removidas: {len(lines) - len(clean_lines)} linhas")

if __name__ == '__main__':
    fix_duplication_definitively()

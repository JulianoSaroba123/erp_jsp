#!/usr/bin/env python3
"""
Script para corrigir rotas duplicadas em os_routes.py
"""

def fix_duplicate_routes():
    file_path = r'c:\Users\julia\Desktop\Backup ERP\erp_jsp_teste\app\ordem_servico\os_routes.py'
    
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Procurar por padrões de duplicação
    # Vamos dividir o conteúdo em linhas e encontrar onde começa a duplicação
    lines = content.split('\n')
    
    # Encontrar onde está a primeira ocorrência de teste_financeiro_os14
    first_occurrence = None
    for i, line in enumerate(lines):
        if 'def teste_financeiro_os14():' in line:
            first_occurrence = i
            break
    
    if first_occurrence is None:
        print("Função não encontrada")
        return
    
    print(f"Primeira ocorrência na linha {first_occurrence + 1}")
    
    # Procurar a segunda ocorrência
    second_occurrence = None
    for i in range(first_occurrence + 1, len(lines)):
        if 'def teste_financeiro_os14():' in lines[i]:
            second_occurrence = i
            break
    
    if second_occurrence is None:
        print("Não há duplicação")
        return
    
    print(f"Segunda ocorrência na linha {second_occurrence + 1}")
    print(f"Removendo linhas {second_occurrence + 1} até o final")
    
    # Remover da segunda ocorrência até o final
    clean_lines = lines[:second_occurrence]
    
    # Remover linhas vazias no final
    while clean_lines and clean_lines[-1].strip() == '':
        clean_lines.pop()
    
    # Escrever arquivo limpo
    clean_content = '\n'.join(clean_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"Arquivo corrigido! Removidas {len(lines) - len(clean_lines)} linhas")
    print(f"Arquivo original: {len(lines)} linhas")
    print(f"Arquivo limpo: {len(clean_lines)} linhas")

if __name__ == '__main__':
    fix_duplicate_routes()

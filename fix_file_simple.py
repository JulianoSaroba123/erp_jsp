#!/usr/bin/env python3
"""
Script para corrigir arquivo duplicado removendo a segunda metade
"""

def fix_file():
    file_path = r'c:\Users\julia\Desktop\Backup ERP\erp_jsp_teste\app\ordem_servico\os_routes.py'
    
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Arquivo original: {len(lines)} linhas")
    
    # Como sabemos que há duplicação, vamos pegar apenas a primeira metade
    half = len(lines) // 2
    first_half = lines[:half]
    
    print(f"Primeira metade: {len(first_half)} linhas")
    
    # Verificar se a primeira metade termina em uma função completa
    # Vamos procurar a última linha que não está indentada (definição de função)
    last_function_line = 0
    for i in range(len(first_half) - 1, -1, -1):
        line = first_half[i]
        if line.startswith('def ') or line.startswith('@os_bp.route'):
            last_function_line = i
            break
    
    print(f"Última função encontrada na linha: {last_function_line + 1}")
    
    # Vamos manter até uma linha após um 'except Exception' completo
    final_lines = []
    in_function = False
    
    for i, line in enumerate(first_half):
        final_lines.append(line)
        
        # Se encontrarmos um except Exception seguido de return/traceback, 
        # e depois uma linha em branco, podemos parar
        if i < len(first_half) - 3:
            current = line.strip()
            next1 = first_half[i+1].strip() if i+1 < len(first_half) else ""
            next2 = first_half[i+2].strip() if i+2 < len(first_half) else ""
            next3 = first_half[i+3].strip() if i+3 < len(first_half) else ""
            
            if (current.startswith('return f"❌ Erro:') and 
                next1 == "" and 
                (next2.startswith('@os_bp.route') or next2.startswith('from flask import'))):
                print(f"Ponto de corte encontrado na linha {i + 1}")
                final_lines = final_lines[:i+2]  # Incluir a linha return e uma linha vazia
                break
    
    # Escrever arquivo corrigido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    
    print(f"Arquivo corrigido!")
    print(f"Linhas finais: {len(final_lines)}")

if __name__ == '__main__':
    fix_file()

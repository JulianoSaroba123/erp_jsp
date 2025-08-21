#!/usr/bin/env python3
"""
Script para encontrar onde começa a duplicação
"""

def find_duplication():
    file_path = r'c:\Users\julia\Desktop\Backup ERP\erp_jsp_teste\app\ordem_servico\os_routes.py'
    
    # Ler arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total de linhas: {len(lines)}")
    
    # Dividir pela metade para comparar
    half = len(lines) // 2
    print(f"Metade: linha {half}")
    
    # Comparar primeira e segunda metade
    for i in range(min(50, half)):  # Comparar primeiras 50 linhas
        line1 = lines[i].strip()
        line2 = lines[half + i].strip()
        
        if line1 == line2:
            print(f"Duplicação detectada na linha {i+1} e {half + i + 1}")
            print(f"Conteúdo: {line1}")
            return i, half + i
    
    print("Não encontrei duplicação simples pela metade")
    
    # Procurar por linhas específicas duplicadas
    for i, line in enumerate(lines):
        if 'from flask import Blueprint' in line and i > 5:
            print(f"Import duplicado na linha {i+1}: {line.strip()}")
            return 0, i
    
    return None, None

if __name__ == '__main__':
    find_duplication()

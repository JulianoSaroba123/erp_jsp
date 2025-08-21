#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para padronizar bordas no template de OS
"""

import re

# Ler arquivo
with open(r'c:\Users\julia\Desktop\erp_jsp\app\ordem_servico\templates\cadastro_os_completo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituições
# 1. Substituir section-header por secao-formulario
content = content.replace('class="section-header"', 'class="secao-formulario"')

# 2. Substituir mb-0 por mb-3 nos títulos
content = content.replace('text-success mb-0', 'text-success mb-3')

# 3. Adicionar fechamentos de div nas seções (buscar padrão e adicionar fechamento)
# Procurar por seções que terminam com </div> seguido de <!-- comentário -->
# e adicionar </div> antes do comentário

sections_pattern = r'(\s+</div>\s*\n\s*)(<!-- \d+\..*? -->)'
content = re.sub(sections_pattern, r'\1</div>\n\n\2', content)

# Salvar arquivo
with open(r'c:\Users\julia\Desktop\erp_jsp\app\ordem_servico\templates\cadastro_os_completo.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Padronização de bordas concluída!")
print("✅ Todas as seções agora usam .secao-formulario")
print("✅ Títulos ajustados para mb-3")
print("✅ Fechamentos de div adicionados")

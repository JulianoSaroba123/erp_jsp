"""
Script para criar um comando SQL simples que pode ser executado para corrigir o cliente no Render.
Este script apenas imprime os comandos SQL necessários sem executá-los.
"""

print("""
-- Comandos SQL para corrigir o status do cliente no Render
-- Copie e cole estes comandos no console do PostgreSQL no Render

-- Primeiro, verificar o cliente
SELECT id, nome, cpf_cnpj, ativo, codigo
FROM clientes
WHERE nome LIKE '%Sergio%Yoshio%' OR cpf_cnpj = '07714278838' OR codigo = 'CL10001';

-- Depois, atualizar o status para ativo
UPDATE clientes
SET ativo = TRUE
WHERE nome LIKE '%Sergio%Yoshio%' OR cpf_cnpj = '07714278838' OR codigo = 'CL10001';

-- Para verificar se a atualização foi aplicada
SELECT id, nome, cpf_cnpj, ativo, codigo
FROM clientes
WHERE nome LIKE '%Sergio%Yoshio%' OR cpf_cnpj = '07714278838' OR codigo = 'CL10001';
""")

-- Adiciona campos separados de endereço na tabela clientes
ALTER TABLE clientes ADD COLUMN cep VARCHAR(10);
ALTER TABLE clientes ADD COLUMN logradouro VARCHAR(150);
ALTER TABLE clientes ADD COLUMN numero VARCHAR(20);
ALTER TABLE clientes ADD COLUMN complemento VARCHAR(100);
ALTER TABLE clientes ADD COLUMN bairro VARCHAR(100);
ALTER TABLE clientes ADD COLUMN cidade VARCHAR(100);
ALTER TABLE clientes ADD COLUMN uf VARCHAR(2);

ALTER TABLE clientes ADD COLUMN codigo VARCHAR(10) UNIQUE;
-- Preencher códigos para clientes já existentes
UPDATE clientes SET codigo = 'CLI' || printf('%04d', id) WHERE codigo IS NULL;

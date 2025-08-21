from app import create_app
from extensoes import db
from ordem_servico.os_model import OrdemServico
from cliente.cliente_model import Cliente

app = create_app()
with app.app_context():
    # Verificar tabelas
    print('Tabela cliente existe:', db.engine.has_table('cliente'))
    print('Tabela ordem_servico existe:', db.engine.has_table('ordem_servico'))
    
    # Verificar clientes
    clientes = Cliente.query.all()
    print(f'Clientes no banco: {len(clientes)}')
    
    # Verificar ordens
    ordens = OrdemServico.query.all()
    print(f'Ordens no banco: {len(ordens)}')
    
    # Se não tem cliente, criar um
    if len(clientes) == 0:
        cliente = Cliente(
            nome='Cliente Teste',
            cpf_cnpj='12345678901',
            telefone='11999999999',
            email='teste@teste.com',
            endereco='Rua Teste',
            ativo=True
        )
        db.session.add(cliente)
        db.session.commit()
        print(f'Cliente criado: {cliente.id}')

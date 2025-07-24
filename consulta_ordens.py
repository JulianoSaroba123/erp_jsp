from app import app
from models.servico_model import Servico
from models.produto_model import Produto

with app.app_context():
    print("=== SERVIÇOS ===")
    servicos = Servico.query.all()
    for s in servicos:
        print(f"ID: {s.id}, Código: {s.codigo}, Nome: {s.nome}, Unidade: {s.unidade}, Valor: {s.valor}, Situação: {s.situacao}")

    print("\n=== PRODUTOS ===")
    produtos = Produto.query.all()
    for p in produtos:
        print(f"ID: {p.id}, Código: {p.codigo}, Nome: {p.nome}, Unidade: {p.unidade}, Estoque: {p.estoque}, Valor Venda: {p.valor_venda}, Valor Compra: {p.valor_compra}, Situação: {p.situacao}")
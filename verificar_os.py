#!/usr/bin/env python3
from app.ordem_servico.os_model import OrdemServico
from app.app import app

with app.app_context():
    print("=== VERIFICACAO DE ORDENS DE SERVICO ===")
    
    # Total de OS
    total = OrdemServico.query.count()
    print(f"Total de OS no banco: {total}")
    
    # Listar todas as OS
    todas_os = OrdemServico.query.order_by(OrdemServico.id.desc()).all()
    
    if todas_os:
        print("\nTodas as OS no banco:")
        for os in todas_os:
            print(f"  ID: {os.id} | Código: {os.codigo} | Cliente: {os.cliente_id} | Valor: R$ {os.valor_total:.2f} | Status: {os.status}")
    else:
        print("Nenhuma OS encontrada")
        
    # Última OS criada
    ultima = OrdemServico.query.order_by(OrdemServico.id.desc()).first()
    if ultima:
        print(f"\nÚltima OS criada:")
        print(f"  ID: {ultima.id}")
        print(f"  Código: {ultima.codigo}")
        print(f"  Cliente ID: {ultima.cliente_id}")
        print(f"  Valor Total: R$ {ultima.valor_total:.2f}")
        print(f"  Valor Serviços: R$ {ultima.valor_servicos:.2f}")
        print(f"  Valor Produtos: R$ {ultima.valor_produtos:.2f}")
        print(f"  Status: {ultima.status}")
        print(f"  Data Emissão: {ultima.data_emissao}")

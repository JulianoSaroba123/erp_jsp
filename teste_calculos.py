#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste dos cálculos da Ordem de Serviço
"""

from app.ordem_servico.os_calculos import CalculadoraOS

def teste_calculo_horas():
    """Testa o cálculo de horas trabalhadas"""
    print("=== TESTE CÁLCULO HORAS ===")
    horas = CalculadoraOS.calcular_horas_trabalhadas("08:00", "17:00")
    print(f"Horas trabalhadas (08:00 às 17:00): {horas}")
    assert horas == 9.0, f"Esperado 9.0, obtido {horas}"
    print("✅ Teste de horas passou!")

def teste_calculo_km():
    """Testa o cálculo de KM total"""
    print("\n=== TESTE CÁLCULO KM ===")
    km = CalculadoraOS.calcular_km_total("100", "250")
    print(f"KM total (inicial: 100, final: 250): {km}")
    assert km == 150.0, f"Esperado 150.0, obtido {km}"
    print("✅ Teste de KM passou!")

def teste_calculo_deslocamento():
    """Testa o cálculo de deslocamento"""
    print("\n=== TESTE CÁLCULO DESLOCAMENTO ===")
    
    # Teste com KM menor que 50 (não deve cobrar)
    valor1 = CalculadoraOS.calcular_valor_deslocamento(30)
    print(f"Deslocamento 30km: R$ {valor1}")
    assert valor1 == 0.0, f"Esperado 0.0, obtido {valor1}"
    
    # Teste com KM maior que 50 (deve cobrar R$1.50/km)
    valor2 = CalculadoraOS.calcular_valor_deslocamento(100)
    print(f"Deslocamento 100km: R$ {valor2}")
    assert valor2 == 150.0, f"Esperado 150.0, obtido {valor2}"
    
    print("✅ Teste de deslocamento passou!")

def teste_calculo_servicos():
    """Testa o cálculo de valor dos serviços"""
    print("\n=== TESTE CÁLCULO SERVIÇOS ===")
    
    servicos_data = [
        {
            "servico_id": "1",
            "nome": "Manutenção",
            "quantidade": 2,
            "valor_unitario": 50.0
        },
        {
            "servico_id": "2", 
            "nome": "Instalação",
            "quantidade": 1,
            "valor_unitario": 80.0
        }
    ]
    
    horas_trabalhadas = 4.0
    valor = CalculadoraOS.calcular_valor_servicos(servicos_data, horas_trabalhadas)
    print(f"Valor serviços: R$ {valor}")
    # (2 * 50.0 * 4.0) + (1 * 80.0 * 4.0) = 400 + 320 = 720
    assert valor == 720.0, f"Esperado 720.0, obtido {valor}"
    print("✅ Teste de serviços passou!")

def teste_calculo_produtos():
    """Testa o cálculo de valor dos produtos"""
    print("\n=== TESTE CÁLCULO PRODUTOS ===")
    
    produtos_data = [
        {
            "produto_id": "1",
            "nome": "Peça A",
            "quantidade": 3,
            "valor_unitario": 25.0
        },
        {
            "produto_id": "2",
            "nome": "Peça B", 
            "quantidade": 1,
            "valor_unitario": 100.0
        }
    ]
    
    valor = CalculadoraOS.calcular_valor_produtos(produtos_data)
    print(f"Valor produtos: R$ {valor}")
    # (3 * 25.0) + (1 * 100.0) = 75 + 100 = 175
    assert valor == 175.0, f"Esperado 175.0, obtido {valor}"
    print("✅ Teste de produtos passou!")

def teste_calculo_total():
    """Testa o cálculo do valor total"""
    print("\n=== TESTE CÁLCULO TOTAL ===")
    
    valor_total = CalculadoraOS.calcular_valor_total(720.0, 175.0, 150.0)
    print(f"Valor total: R$ {valor_total}")
    # 720 + 175 + 150 = 1045
    assert valor_total == 1045.0, f"Esperado 1045.0, obtido {valor_total}"
    print("✅ Teste de total passou!")

def teste_calcular_todos_valores():
    """Testa o cálculo de todos os valores de uma vez"""
    print("\n=== TESTE CÁLCULO COMPLETO ===")
    
    dados_form = {
        'hora_inicio': '08:00',
        'hora_termino': '12:00',
        'km_inicial': '100',
        'km_final': '200'
    }
    
    servicos_data = [
        {
            "servico_id": "1",
            "nome": "Teste",
            "quantidade": 1,
            "valor_unitario": 50.0
        }
    ]
    
    produtos_data = [
        {
            "produto_id": "1", 
            "nome": "Produto Teste",
            "quantidade": 2,
            "valor_unitario": 30.0
        }
    ]
    
    resultado = CalculadoraOS.calcular_todos_valores(dados_form, servicos_data, produtos_data)
    
    print(f"Resultado completo: {resultado}")
    
    # Verificar se todos os campos estão presentes
    campos_esperados = ['total_horas', 'km_total', 'valor_deslocamento', 
                       'valor_servicos', 'valor_produtos', 'valor_total']
    
    for campo in campos_esperados:
        assert campo in resultado, f"Campo {campo} não encontrado no resultado"
    
    # Verificar valores específicos
    assert resultado['total_horas'] == 4.0, f"Horas incorretas: {resultado['total_horas']}"
    assert resultado['km_total'] == 100.0, f"KM incorreto: {resultado['km_total']}"
    assert resultado['valor_deslocamento'] == 150.0, f"Deslocamento incorreto: {resultado['valor_deslocamento']}"
    assert resultado['valor_servicos'] == 200.0, f"Serviços incorreto: {resultado['valor_servicos']}"  # 1 * 50 * 4
    assert resultado['valor_produtos'] == 60.0, f"Produtos incorreto: {resultado['valor_produtos']}"  # 2 * 30
    assert resultado['valor_total'] == 410.0, f"Total incorreto: {resultado['valor_total']}"  # 200 + 60 + 150
    
    print("✅ Teste completo passou!")

if __name__ == "__main__":
    try:
        print("🚀 INICIANDO TESTES DOS CÁLCULOS DA OS")
        
        teste_calculo_horas()
        teste_calculo_km()
        teste_calculo_deslocamento()
        teste_calculo_servicos()
        teste_calculo_produtos()
        teste_calculo_total()
        teste_calcular_todos_valores()
        
        print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("✅ Os cálculos estão funcionando corretamente.")
        print("✅ O backend está pronto para salvar os totais no banco de dados.")
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()

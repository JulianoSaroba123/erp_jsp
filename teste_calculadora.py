#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from ordem_servico.os_calculos import CalculadoraOS

def testar_calculadora():
    """Teste isolado da calculadora"""
    
    print("=== TESTE DA CALCULADORA ===")
    
    # Dados de teste
    dados_form = {
        'hora_inicio': '08:00',
        'hora_termino': '12:00',
        'km_inicial': '1000',
        'km_final': '1050'
    }
    
    servicos_data = [
        {"id": 1, "nome": "Formatação", "valor_unitario": 150.00, "quantidade": 1}
    ]
    
    produtos_data = [
        {"id": 1, "nome": "HD 1TB", "valor_unitario": 300.00, "quantidade": 1}
    ]
    
    print(f"Dados do formulário: {dados_form}")
    print(f"Serviços: {servicos_data}")
    print(f"Produtos: {produtos_data}")
    
    try:
        # Testar cálculos individuais
        print("\n--- Cálculos Individuais ---")
        
        horas = CalculadoraOS.calcular_horas_trabalhadas(
            dados_form.get('hora_inicio'),
            dados_form.get('hora_termino')
        )
        print(f"Horas trabalhadas: {horas}")
        
        km_total = CalculadoraOS.calcular_km_total(
            dados_form.get('km_inicial'),
            dados_form.get('km_final')
        )
        print(f"KM total: {km_total}")
        
        valor_deslocamento = CalculadoraOS.calcular_valor_deslocamento(km_total)
        print(f"Valor deslocamento: {valor_deslocamento}")
        
        valor_servicos = CalculadoraOS.calcular_valor_servicos(servicos_data, horas)
        print(f"Valor serviços: {valor_servicos}")
        print(f"Debug - servicos_data recebidos: {servicos_data}")
        print(f"Debug - horas recebidas: {horas}")
        
        valor_produtos = CalculadoraOS.calcular_valor_produtos(produtos_data)
        print(f"Valor produtos: {valor_produtos}")
        print(f"Debug - produtos_data recebidos: {produtos_data}")
        
        # Testar função completa
        print("\n--- Cálculo Completo ---")
        calculos = CalculadoraOS.calcular_todos_valores(
            dados_form, 
            servicos_data, 
            produtos_data
        )
        
        print(f"Resultado completo: {calculos}")
        
    except Exception as e:
        print(f"❌ Erro na calculadora: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_calculadora()

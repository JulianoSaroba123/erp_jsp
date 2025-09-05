# Integração Financeira - Ordens de Serviço

## 📋 Visão Geral

Esta integração permite que Ordens de Serviço (OS) gerem automaticamente lançamentos financeiros quando marcadas como pagas, suportando diferentes condições de pagamento.

## 🎯 Funcionalidades

### ✅ Condições de Pagamento Suportadas
- **À Vista**: Gera um único lançamento para hoje
- **Parcelado**: Gera N parcelas a cada 30 dias
- **Com Entrada**: Permite definir valor de entrada + parcelas
- **Cronograma Personalizado**: Datas e valores totalmente customizáveis

### ✅ Características Técnicas
- **Idempotente**: Executar várias vezes não duplica lançamentos
- **Transacional**: Todas as operações em uma única transação
- **Auditável**: Logs detalhados de todas as operações
- **Flexível**: Suporte a diferentes formas de pagamento

## 🏗️ Arquitetura

### Modelos
```
LancamentoFinanceiroOS
├── id (PK)
├── os_id (FK para OrdemServico)
├── descricao
├── valor (Decimal)
├── data_vencimento
├── data_pagamento
├── forma_pagamento
├── status (Pendente|Pago)
├── parcela (0=entrada, 1..N=parcelas)
├── total_parcelas
└── origem (sempre "OS")
```

### Novos Campos em OrdemServico
```
OrdemServico (campos adicionais)
├── condicao_pagamento ("avista" | "parcelado")
├── qtd_parcelas (Integer)
├── valor_entrada (Decimal)
├── status_pagamento ("pendente" | "pago")
└── schedule_json (JSON de cronograma personalizado)
```

## 🚀 Como Usar

### 1. No Código (Programaticamente)

```python
from app.financeiro.lancamento_os_service import gerar_lancamentos_financeiro
from decimal import Decimal

# Pagamento à vista
lancamentos = gerar_lancamentos_financeiro(
    os=ordem_servico,
    forma_pagamento="PIX",
    valor_total=Decimal("1000.00"),
    parcelas=1
)

# Parcelado com entrada
lancamentos = gerar_lancamentos_financeiro(
    os=ordem_servico,
    forma_pagamento="Cartão",
    valor_total=Decimal("1000.00"),
    parcelas=3,
    entrada=Decimal("300.00")
)

# Cronograma personalizado
from datetime import date, timedelta
schedule = [
    (Decimal("500.00"), date.today()),
    (Decimal("300.00"), date.today() + timedelta(days=15)),
    (Decimal("200.00"), date.today() + timedelta(days=45))
]

lancamentos = gerar_lancamentos_financeiro(
    os=ordem_servico,
    forma_pagamento="Boleto",
    valor_total=Decimal("1000.00"),
    schedule_custom=schedule
)
```

### 2. Via Interface Web

1. **Editar OS**: Acesse a tela de edição da OS
2. **Definir Pagamento**: Configure:
   - Condição de pagamento (À vista / Parcelado)
   - Forma de pagamento (PIX, Cartão, etc.)
   - Quantidade de parcelas (se parcelado)
   - Valor de entrada (opcional)
3. **Marcar como Pago**: Altere o status de pagamento para "Pago"
4. **Salvar**: Os lançamentos serão criados automaticamente

### 3. Modal "Editar Parcelas" (Futuro)

Interface avançada para:
- Personalizar datas de vencimento
- Ajustar valores individuais
- Distribuição automática em 30/60/90 dias
- Salvar cronograma personalizado

## 🧪 Testes

### Executar Testes de Integração
```bash
python test_integracao_financeira.py
```

### Aplicar Migrações
```bash
python aplicar_migracao_financeira.py
# ou
alembic upgrade head
```

### Exemplo de Uso
```bash
python exemplo_integracao_financeira.py
```

## 📊 Fluxo de Funcionamento

### Automático (via Interface)
```
OS Criada → Editada → Status="Concluída" + Pagamento="Pago" → 
Hook Executado → Lançamentos Gerados → Visualização Atualizada
```

### Manual (via API/Código)
```
Chamada para gerar_lancamentos_financeiro() → 
Remove Lançamentos Existentes → Calcula Parcelas → 
Cria Novos Lançamentos → Commit no BD
```

## 🔍 Monitoramento e Logs

### Logs Importantes
- `INFO: Gerando lançamentos financeiros para OS ID: X`
- `INFO: Removendo lançamentos financeiros existentes`
- `INFO: Total de N lançamentos financeiros criados`

### Validações Automáticas
- ✅ Soma das parcelas = valor total
- ✅ Parcelas ≥ 1
- ✅ Valores > 0
- ✅ Datas válidas

## 🚨 Tratamento de Erros

### Cenários Cobertos
- **OS não encontrada**: Erro com mensagem clara
- **Dados inválidos**: Validação antes da criação
- **Falha na transação**: Rollback automático
- **Conflitos de concorrência**: Locks adequados

### Recuperação
- **Idempotência**: Re-executar corrige inconsistências
- **Logs detalhados**: Facilita debugging
- **Transações atômicas**: Estado sempre consistente

## 🎯 Roadmap

### Próximas Features
- [ ] Interface para edição de parcelas
- [ ] Integração com módulo de cobrança
- [ ] Notificações de vencimento
- [ ] Relatórios financeiros por OS
- [ ] Dashboard de recebimentos

### Melhorias Técnicas
- [ ] Cache de cálculos
- [ ] Processamento assíncrono
- [ ] Webhooks para eventos financeiros
- [ ] API REST completa

## 📞 Suporte

### Problemas Comuns

**1. Lançamentos duplicados**
- Solução: A função é idempotente, execute novamente

**2. Valores não conferem**
- Verifique se `valor_total` está correto
- Confirme entrada + parcelas = total

**3. Migração falhou**
- Execute: `python aplicar_migracao_financeira.py`
- Ou: `alembic upgrade head`

### Debug
```python
# Verificar lançamentos de uma OS
from app.financeiro.lancamento_os_model import LancamentoFinanceiroOS
lancamentos = LancamentoFinanceiroOS.query.filter_by(os_id=123).all()
for l in lancamentos:
    print(f"{l.descricao} - R$ {l.valor} - {l.status}")
```

---
*Documentação gerada em {{ date.today() }}*

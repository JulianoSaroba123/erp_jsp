// os_calculos.js - Cálculos da Ordem de Serviço

// Variáveis globais para armazenar dados
let servicos = [];
let produtos = [];
let parcelas = [];

// Função para calcular horas trabalhadas
function calcularHoras() {
    const inicio = document.getElementById('hora_inicio').value;
    const termino = document.getElementById('hora_termino').value;
    
    if (inicio && termino) {
        const [horaIni, minIni] = inicio.split(':').map(Number);
        const [horaTerm, minTerm] = termino.split(':').map(Number);
        
        const inicioMinutos = horaIni * 60 + minIni;
        const terminoMinutos = horaTerm * 60 + minTerm;
        
        let diferencaMinutos;
        if (terminoMinutos >= inicioMinutos) {
            diferencaMinutos = terminoMinutos - inicioMinutos;
        } else {
            // Caso passe da meia-noite
            diferencaMinutos = (24 * 60) - inicioMinutos + terminoMinutos;
        }
        
        const horas = Math.floor(diferencaMinutos / 60);
        const minutos = diferencaMinutos % 60;
        
        const totalHoras = horas + (minutos / 60);
        document.getElementById('total_horas').value = totalHoras.toFixed(2) + 'h';
        
        calcularTotais();
        return totalHoras;
    }
    
    document.getElementById('total_horas').value = '';
    return 0;
}

// Função para calcular deslocamento
function calcularDeslocamento() {
    const kmInicial = parseFloat(document.getElementById('km_inicial').value) || 0;
    const kmFinal = parseFloat(document.getElementById('km_final').value) || 0;
    
    if (kmFinal >= kmInicial) {
        const kmTotal = kmFinal - kmInicial;
        const valorKm = 1.50; // R$ 1,50 por km
        const valorDeslocamento = kmTotal * valorKm;
        
        document.getElementById('km_total').value = kmTotal.toFixed(1) + ' km';
        document.getElementById('valor_deslocamento_display').value = 'R$ ' + valorDeslocamento.toFixed(2);
        document.getElementById('valor_deslocamento').value = valorDeslocamento.toFixed(2);
        
        calcularTotais();
        return valorDeslocamento;
    }
    
    document.getElementById('km_total').value = '';
    document.getElementById('valor_deslocamento_display').value = '';
    document.getElementById('valor_deslocamento').value = '0';
    
    calcularTotais();
    return 0;
}

// Função para adicionar serviço
function adicionarServico() {
    const select = document.getElementById('servico_select');
    const quantidade = parseFloat(document.getElementById('servico_quantidade').value) || 1;
    
    if (!select.value) {
        alert('Selecione um serviço');
        return;
    }
    
    const option = select.options[select.selectedIndex];
    const servicoId = select.value;
    const nome = option.dataset.nome;
    const valorUnitario = parseFloat(option.dataset.valor) || 0;
    const valorTotal = valorUnitario * quantidade;
    
    // Verificar se já existe
    const existe = servicos.find(s => s.id === servicoId);
    if (existe) {
        existe.quantidade += quantidade;
        existe.valor_total = existe.valor_unitario * existe.quantidade;
    } else {
        servicos.push({
            id: servicoId,
            nome: nome,
            quantidade: quantidade,
            valor_unitario: valorUnitario,
            valor_total: valorTotal
        });
    }
    
    // Resetar campos
    select.value = '';
    document.getElementById('servico_quantidade').value = '1';
    
    atualizarListaServicos();
    calcularTotais();
}

// Função para remover serviço
function removerServico(index) {
    servicos.splice(index, 1);
    atualizarListaServicos();
    calcularTotais();
}

// Função para atualizar lista de serviços
function atualizarListaServicos() {
    const lista = document.getElementById('lista-servicos');
    
    if (servicos.length === 0) {
        lista.innerHTML = '';
        return;
    }
    
    let html = '<h6 class="text-success mb-3">Serviços Adicionados:</h6>';
    
    servicos.forEach((servico, index) => {
        html += `
            <div class="item-row">
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <strong>${servico.nome}</strong>
                    </div>
                    <div class="col-md-2">
                        Qtd: ${servico.quantidade}
                    </div>
                    <div class="col-md-3">
                        Valor Unit.: R$ ${servico.valor_unitario.toFixed(2)}
                    </div>
                    <div class="col-md-2">
                        <strong>R$ ${servico.valor_total.toFixed(2)}</strong>
                    </div>
                    <div class="col-md-1">
                        <button type="button" class="btn btn-danger btn-sm" onclick="removerServico(${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    lista.innerHTML = html;
}

// Função para adicionar produto
function adicionarProduto() {
    const select = document.getElementById('produto_select');
    const quantidade = parseFloat(document.getElementById('produto_quantidade').value) || 1;
    const valorUnitario = parseFloat(document.getElementById('produto_valor').value) || 0;
    
    if (!select.value) {
        alert('Selecione um produto');
        return;
    }
    
    if (valorUnitario <= 0) {
        alert('Informe o valor unitário');
        return;
    }
    
    const option = select.options[select.selectedIndex];
    const produtoId = select.value;
    const nome = option.dataset.nome;
    const valorTotal = valorUnitario * quantidade;
    
    // Verificar se já existe
    const existe = produtos.find(p => p.id === produtoId);
    if (existe) {
        existe.quantidade += quantidade;
        existe.valor_total = existe.valor_unitario * existe.quantidade;
    } else {
        produtos.push({
            id: produtoId,
            nome: nome,
            quantidade: quantidade,
            valor_unitario: valorUnitario,
            valor_total: valorTotal
        });
    }
    
    // Resetar campos
    select.value = '';
    document.getElementById('produto_quantidade').value = '1';
    document.getElementById('produto_valor').value = '';
    
    atualizarListaProdutos();
    calcularTotais();
}

// Função para remover produto
function removerProduto(index) {
    produtos.splice(index, 1);
    atualizarListaProdutos();
    calcularTotais();
}

// Função para atualizar lista de produtos
function atualizarListaProdutos() {
    const lista = document.getElementById('lista-produtos');
    
    if (produtos.length === 0) {
        lista.innerHTML = '';
        return;
    }
    
    let html = '<h6 class="text-success mb-3">Produtos Adicionados:</h6>';
    
    produtos.forEach((produto, index) => {
        html += `
            <div class="item-row">
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <strong>${produto.nome}</strong>
                    </div>
                    <div class="col-md-2">
                        Qtd: ${produto.quantidade}
                    </div>
                    <div class="col-md-3">
                        Valor Unit.: R$ ${produto.valor_unitario.toFixed(2)}
                    </div>
                    <div class="col-md-2">
                        <strong>R$ ${produto.valor_total.toFixed(2)}</strong>
                    </div>
                    <div class="col-md-1">
                        <button type="button" class="btn btn-danger btn-sm" onclick="removerProduto(${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    lista.innerHTML = html;
}

// Função para calcular totais
function calcularTotais() {
    // Calcular valor dos serviços
    const valorServicos = servicos.reduce((total, servico) => total + servico.valor_total, 0);
    
    // Calcular valor dos produtos
    const valorProdutos = produtos.reduce((total, produto) => total + produto.valor_total, 0);
    
    // Valor do deslocamento
    const valorDeslocamento = parseFloat(document.getElementById('valor_deslocamento').value) || 0;
    
    // Valor total
    const valorTotal = valorServicos + valorProdutos + valorDeslocamento;
    
    // Atualizar campos
    document.getElementById('valor_servicos_display').value = 'R$ ' + valorServicos.toFixed(2);
    document.getElementById('valor_servicos').value = valorServicos.toFixed(2);
    
    document.getElementById('valor_produtos_display').value = 'R$ ' + valorProdutos.toFixed(2);
    document.getElementById('valor_produtos').value = valorProdutos.toFixed(2);
    
    document.getElementById('valor_total_display').value = 'R$ ' + valorTotal.toFixed(2);
    document.getElementById('valor_total').value = valorTotal.toFixed(2);
    
    // Se houver parcelas, recalcular
    if (parcelas.length > 0) {
        gerarParcelas();
    }
}

// Função para formatar moeda
function formatarMoeda(valor) {
    return 'R$ ' + parseFloat(valor || 0).toFixed(2).replace('.', ',');
}
  
  if (isNaN(h1) || isNaN(m1) || isNaN(h2) || isNaN(m2)) {
    document.getElementById('total_horas').value = '';
    calcularValoresOS();
    return;
  }
  
  let diff = (h2 * 60 + m2) - (h1 * 60 + m1);
  diff = diff < 0 ? 0 : diff;
  const horasDecimais = (diff / 60).toFixed(2);
  document.getElementById('total_horas').value = horasDecimais;
  calcularValoresOS();
}

// Funções de Cálculo de Quilometragem
function calcularKmTotal() {
  const ki = parseFloat(document.getElementById('km_inicial').value) || 0;
  const kf = parseFloat(document.getElementById('km_final').value) || 0;
  const kmTotal = kf >= ki ? (kf - ki).toFixed(1) : '';
  document.getElementById('km_total').value = kmTotal;
  calcularValorDeslocamento();
}

function calcularValorDeslocamento() {
  const km = parseFloat(document.getElementById('km_total').value) || 0;
  let valorDeslocamento = 0;
  
  // Tabela de referência de deslocamento
  const tabelaDeslocamento = [
    {limite: 10, valor: 25},
    {limite: 20, valor: 44},
    {limite: 30, valor: 66},
    {limite: 40, valor: 88},
    {limite: 50, valor: 110},
    {limite: 60, valor: 132},
    {limite: 70, valor: 154},
    {limite: 80, valor: 176},
    {limite: 90, valor: 198},
    {limite: 100, valor: 220},
    {limite: 110, valor: 242},
    {limite: 120, valor: 264},
    {limite: 130, valor: 286},
    {limite: 140, valor: 308},
    {limite: 150, valor: 330}
  ];
  
  // Encontra o valor baseado na quilometragem
  for (let faixa of tabelaDeslocamento) {
    if (km <= faixa.limite) {
      valorDeslocamento = faixa.valor;
      break;
    }
  }
  
  // Se exceder 150km, cobra R$2 por km adicional
  if (km > 150) {
    valorDeslocamento = 330 + ((km - 150) * 2);
  }
  
  document.getElementById('valor_deslocamento').value = valorDeslocamento.toFixed(2);
  calcularValoresOS();
}

// Função Principal de Cálculo de Valores
function calcularValoresOS() {
  // Serviços já adicionados
  let somaServicos = listaServicos.reduce((a, i) => a + i.qtd * i.valor, 0);
  
  // Serviço que está sendo digitado (mas ainda não adicionado)
  const qtd = parseInt(document.getElementById('servico_qtd').value) || 0;
  const valor = parseFloat(document.getElementById('servico_valor').value) || 0;
  const nome = document.getElementById('servico_nome').value;
  if (nome && qtd > 0 && valor > 0) {
    somaServicos += qtd * valor;
  }
  
  // Lógica de cobrança por hora
  let valorServicos = somaServicos;
  if (document.getElementById('cobranca_hora').checked) {
    const totalHoras = parseFloat(document.getElementById('total_horas').value.replace(',', '.')) || 0;
    valorServicos = somaServicos * totalHoras;
  }
  
  // Produtos
  const valorProdutos = listaProdutos.reduce((a, i) => a + i.qtd * i.valor, 0);
  
  // Deslocamento
  const valorDeslocamento = parseFloat(document.getElementById('valor_deslocamento').value) || 0;
  
  // Atualiza os campos
  document.getElementById('valor_servicos').value = valorServicos.toFixed(2);
  document.getElementById('valor_produtos').value = valorProdutos.toFixed(2);
  document.getElementById('valor_total').value = (valorServicos + valorProdutos + valorDeslocamento).toFixed(2);
}

// Função para atualizar tipo de cobrança
function atualizarTipoCobranca() {
  const hora = document.getElementById('cobranca_hora');
  const fechado = document.getElementById('cobranca_fechado');
  
  if (event.target === hora && hora.checked) fechado.checked = false;
  if (event.target === fechado && fechado.checked) hora.checked = false;
  
  document.getElementById('tipo_cobranca').value = hora.checked ? 'hora' : 'fechado';
  calcularValoresOS();
}

// Função para toggle da tabela de referência
function toggleTabelaReferencia() {
  const tbl = document.getElementById('tabela-referencia');
  const btn = document.getElementById('btn-toggle-tabela');
  
  if (tbl.style.display === 'none') {
    tbl.style.display = 'block';
    btn.innerHTML = '<i class="fas fa-table"></i> Ocultar Tabela de Referência de Deslocamento';
  } else {
    tbl.style.display = 'none';
    btn.innerHTML = '<i class="fas fa-table"></i> Mostrar Tabela de Referência de Deslocamento';
  }
}

// Exportar funções principais
window.calcularValoresOS = calcularValoresOS;
window.calcularTotalHorasDecimal = calcularTotalHorasDecimal;
window.calcularKmTotal = calcularKmTotal;
window.atualizarTipoCobranca = atualizarTipoCobranca;
window.toggleTabelaReferencia = toggleTabelaReferencia;

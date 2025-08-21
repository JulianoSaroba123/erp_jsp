// os_formulario.js - Módulo Principal do Formulário de Ordem de Serviço

// Aguarda o DOM estar carregado
document.addEventListener('DOMContentLoaded', function() {
  // Inicializar dados salvos se existirem
  const servicosJson = document.getElementById('servicos_json').value;
  const produtosJson = document.getElementById('produtos_json').value;
  
  if (servicosJson) {
    try {
      listaServicos = JSON.parse(servicosJson);
    } catch (e) {
      listaServicos = [];
    }
  }
  
  if (produtosJson) {
    try {
      listaProdutos = JSON.parse(produtosJson);
    } catch (e) {
      listaProdutos = [];
    }
  }
  
  // Configurar eventos
  configurarEventos();
  
  // Atualizar tabelas iniciais
  atualizarTabelaServicos();
  atualizarTabelaProdutos();
  
  // Configurar tipo de cobrança inicial
  const tipoCobranca = document.getElementById('tipo_cobranca').value;
  if (tipoCobranca === 'hora') {
    document.getElementById('cobranca_hora').checked = true;
    document.getElementById('cobranca_fechado').checked = false;
  } else {
    document.getElementById('cobranca_hora').checked = false;
    document.getElementById('cobranca_fechado').checked = true;
  }
  
  // Configurar parcelas
  toggleParcelas();
  
  // Se existe campo total_horas em formato HH:MM, converte para decimal
  const totalHorasInput = document.getElementById('total_horas');
  if (totalHorasInput && totalHorasInput.value && totalHorasInput.value.includes(':')) {
    const [h, m] = totalHorasInput.value.split(':').map(Number);
    if (!isNaN(h) && !isNaN(m)) {
      totalHorasInput.value = (h + m/60).toFixed(2);
    }
  }
  
  // Calcular valores iniciais
  calcularValoresOS();
});

// Configurar todos os eventos do formulário
function configurarEventos() {
  // Eventos de tempo
  document.getElementById('hora_inicio').addEventListener('input', calcularTotalHorasDecimal);
  document.getElementById('hora_termino').addEventListener('input', calcularTotalHorasDecimal);
  
  // Eventos de quilometragem
  document.getElementById('km_inicial').addEventListener('input', calcularKmTotal);
  document.getElementById('km_final').addEventListener('input', calcularKmTotal);
  
  // Eventos de cliente
  document.getElementById('cliente_id').addEventListener('change', preencherDadosCliente);
  
  // Eventos de autopreenchimento
  document.getElementById('servico_nome').addEventListener('input', autopreencherServicoValor);
  document.getElementById('produto_nome').addEventListener('input', autopreencherProdutoValor);
  
  // Eventos de adição
  document.getElementById('btn-add-servico').addEventListener('click', function(e) {
    e.preventDefault();
    adicionarServico();
  });
  
  document.getElementById('btn-add-produto').addEventListener('click', function(e) {
    e.preventDefault();
    adicionarProduto();
  });
  
  // Eventos de cálculo em tempo real
  ['servico_nome', 'servico_qtd', 'servico_valor', 'total_horas', 'valor_produtos', 'valor_deslocamento'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', calcularValoresOS);
  });
  
  ['cobranca_hora', 'cobranca_fechado'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', calcularValoresOS);
  });
  
  // Evento da tabela de referência
  document.getElementById('btn-toggle-tabela').addEventListener('click', function(e) {
    e.preventDefault();
    toggleTabelaReferencia();
  });
  
  // Evento de condições de pagamento
  document.getElementById('condicoes_pagamento').addEventListener('change', toggleParcelas);
}

// Preencher dados do cliente selecionado
function preencherDadosCliente() {
  const select = document.getElementById('cliente_id');
  const option = select.options[select.selectedIndex];
  
  if (option && option.value) {
    document.getElementById('cpf').value = option.getAttribute('data-cpf') || '';
    document.getElementById('telefone').value = option.getAttribute('data-telefone') || '';
    document.getElementById('email').value = option.getAttribute('data-email') || '';
    document.getElementById('endereco').value = option.getAttribute('data-endereco') || '';
  } else {
    document.getElementById('cpf').value = '';
    document.getElementById('telefone').value = '';
    document.getElementById('email').value = '';
    document.getElementById('endereco').value = '';
  }
}

// Autopreencher valor do serviço
function autopreencherServicoValor() {
  const nome = document.getElementById('servico_nome').value;
  const options = document.querySelectorAll('#lista_servicos option');
  
  options.forEach(opt => {
    if (opt.value === nome) {
      const valor = parseFloat(opt.dataset.valor || 0);
      document.getElementById('servico_valor').value = valor.toFixed(2);
      calcularValoresOS();
    }
  });
}

// Autopreencher valor do produto
function autopreencherProdutoValor() {
  const nome = document.getElementById('produto_nome').value;
  const options = document.querySelectorAll('#lista_produtos option');
  
  options.forEach(opt => {
    if (opt.value === nome) {
      const valor = parseFloat(opt.dataset.valor || 0);
      document.getElementById('produto_valor').value = valor.toFixed(2);
      calcularValoresOS();
    }
  });
}

// Adicionar serviço à lista
function adicionarServico() {
  const nome = document.getElementById('servico_nome').value;
  const qtd = parseInt(document.getElementById('servico_qtd').value) || 1;
  const valor = parseFloat(document.getElementById('servico_valor').value) || 0;
  const totalHorasStr = document.getElementById('total_horas').value;
  
  let qtd_horas = 0;
  if (totalHorasStr && totalHorasStr.includes(':')) {
    const [h, m] = totalHorasStr.split(':').map(Number);
    qtd_horas = h + (m/60);
  } else {
    qtd_horas = parseFloat(totalHorasStr.replace(',', '.')) || 0;
  }
  
  if (nome && valor > 0) {
    listaServicos.push({nome, qtd, valor, qtd_horas});
    atualizarTabelaServicos();
    limparCamposServico();
  }
}

// Adicionar produto à lista
function adicionarProduto() {
  const nome = document.getElementById('produto_nome').value;
  const qtd = parseInt(document.getElementById('produto_qtd').value) || 1;
  const valor = parseFloat(document.getElementById('produto_valor').value) || 0;
  
  if (nome && valor > 0) {
    listaProdutos.push({nome, qtd, valor});
    atualizarTabelaProdutos();
    limparCamposProduto();
  }
}

// Remover serviço da lista
function removerServico(index) {
  listaServicos.splice(index, 1);
  atualizarTabelaServicos();
}

// Remover produto da lista
function removerProduto(index) {
  listaProdutos.splice(index, 1);
  atualizarTabelaProdutos();
}

// Atualizar tabela de serviços
function atualizarTabelaServicos() {
  const tbody = document.querySelector('#tabela-servicos tbody');
  tbody.innerHTML = '';
  
  listaServicos.forEach((item, idx) => {
    tbody.insertAdjacentHTML('beforeend', `
      <tr>
        <td>${item.nome}</td>
        <td>${item.qtd}</td>
        <td>R$ ${item.valor.toFixed(2)}</td>
        <td>R$ ${(item.qtd * item.valor).toFixed(2)}</td>
        <td class="text-center">
          <button class="btn btn-danger btn-sm" onclick="removerServico(${idx})" type="button">
            <i class="fas fa-times"></i>
          </button>
        </td>
      </tr>
    `);
  });
  
  document.getElementById('servicos_json').value = JSON.stringify(listaServicos);
  calcularValoresOS();
}

// Atualizar tabela de produtos
function atualizarTabelaProdutos() {
  const tbody = document.querySelector('#tabela-produtos tbody');
  tbody.innerHTML = '';
  
  listaProdutos.forEach((item, idx) => {
    tbody.insertAdjacentHTML('beforeend', `
      <tr>
        <td>${item.nome}</td>
        <td>${item.qtd}</td>
        <td>R$ ${item.valor.toFixed(2)}</td>
        <td>R$ ${(item.qtd * item.valor).toFixed(2)}</td>
        <td class="text-center">
          <button class="btn btn-danger btn-sm" onclick="removerProduto(${idx})" type="button">
            <i class="fas fa-times"></i>
          </button>
        </td>
      </tr>
    `);
  });
  
  document.getElementById('produtos_json').value = JSON.stringify(listaProdutos);
  calcularValoresOS();
}

// Limpar campos de serviço
function limparCamposServico() {
  document.getElementById('servico_nome').value = '';
  document.getElementById('servico_qtd').value = '1';
  document.getElementById('servico_valor').value = '';
}

// Limpar campos de produto
function limparCamposProduto() {
  document.getElementById('produto_nome').value = '';
  document.getElementById('produto_qtd').value = '1';
  document.getElementById('produto_valor').value = '';
}

// Limpar formulário completo
function limparFormulario() {
  if (confirm('Tem certeza que deseja limpar todos os dados do formulário?')) {
    document.querySelector('form').reset();
    listaServicos = [];
    listaProdutos = [];
    parcelas = [];
    atualizarTabelaServicos();
    atualizarTabelaProdutos();
    renderParcelas();
    calcularValoresOS();
  }
}

// Exportar funções principais
window.removerServico = removerServico;
window.removerProduto = removerProduto;
window.limparFormulario = limparFormulario;

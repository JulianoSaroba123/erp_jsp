// os_parcelas.js - Módulo de Gerenciamento de Parcelas da Ordem de Serviço

let parcelas = [];

// Renderiza as parcelas na tabela
function renderParcelas() {
  const container = document.getElementById('parcelas-list');
  container.innerHTML = '';
  
  parcelas.forEach((p, i) => {
    container.innerHTML += `
      <tr>
        <td>
          <input type="date" class="form-control form-control-sm" value="${p.data}" 
                 onchange="atualizarParcela(${i}, 'data', this.value)">
        </td>
        <td>
          <input type="number" class="form-control form-control-sm" placeholder="Valor" 
                 value="${p.valor}" min="0" step="0.01" 
                 onchange="atualizarParcela(${i}, 'valor', this.value)">
        </td>
        <td class="text-center">
          <button type="button" class="btn btn-danger btn-sm" onclick="removerParcela(${i})">
            <i class="fas fa-times"></i>
          </button>
        </td>
      </tr>
    `;
  });
  
  document.getElementById('parcelas_json').value = JSON.stringify(parcelas);
}

// Adiciona nova parcela
function adicionarParcela(data = '', valor = '') {
  parcelas.push({data: data, valor: valor});
  renderParcelas();
}

// Remove parcela
function removerParcela(i) {
  parcelas.splice(i, 1);
  renderParcelas();
}

// Atualiza uma parcela específica
function atualizarParcela(i, campo, valor) {
  parcelas[i][campo] = valor;
  renderParcelas();
}

// Gera parcelas automaticamente por quantidade
function gerarParcelasPorQuantidade() {
  const qtd = parseInt(document.getElementById('qtd_parcelas').value) || 0;
  const valorTotal = parseFloat(document.getElementById('valor_total').value.replace(',', '.')) || 0;
  
  if (qtd > 0) {
    parcelas = [];
    
    if (valorTotal > 0) {
      const valorParcela = (valorTotal / qtd).toFixed(2);
      for (let i = 0; i < qtd; i++) {
        parcelas.push({data: '', valor: valorParcela});
      }
    } else {
      for (let i = 0; i < qtd; i++) {
        parcelas.push({data: '', valor: ''});
      }
    }
    
    renderParcelas();
  }
}

// Toggle exibição das parcelas
function toggleParcelas() {
  const condicao = document.getElementById('condicoes_pagamento').value;
  const sec = document.getElementById('parcelas-section');
  
  if (condicao === 'Parcelado') {
    sec.style.display = 'block';
    // Se não houver parcelas, adiciona uma por padrão
    if (parcelas.length === 0) {
      adicionarParcela();
    }
  } else {
    sec.style.display = 'none';
    parcelas = [];
    renderParcelas();
  }
}

// Inicializar parcelas com dados existentes
function inicializarParcelas(parcelasSalvas = []) {
  try {
    parcelas = parcelasSalvas || [];
    if (parcelas.length) {
      document.getElementById('qtd_parcelas').value = parcelas.length;
    }
  } catch (e) {
    parcelas = [];
  }
  renderParcelas();
}

// Exportar funções principais
window.renderParcelas = renderParcelas;
window.adicionarParcela = adicionarParcela;
window.removerParcela = removerParcela;
window.atualizarParcela = atualizarParcela;
window.gerarParcelasPorQuantidade = gerarParcelasPorQuantidade;
window.toggleParcelas = toggleParcelas;
window.inicializarParcelas = inicializarParcelas;

// os_formulario_novo.js - Funcionalidades do Formulário de OS

// Função para preencher dados do cliente automaticamente
function preencherDadosCliente() {
    const select = document.getElementById('cliente_id');
    const option = select.options[select.selectedIndex];
    
    if (option.value) {
        document.getElementById('cpf').value = option.dataset.cpf || '';
        document.getElementById('telefone').value = option.dataset.telefone || '';
        document.getElementById('email').value = option.dataset.email || '';
        document.getElementById('endereco').value = option.dataset.endereco || '';
    } else {
        document.getElementById('cpf').value = '';
        document.getElementById('telefone').value = '';
        document.getElementById('email').value = '';
        document.getElementById('endereco').value = '';
    }
}

// Função para preencher valor do produto automaticamente
function preencherValorProduto() {
    const select = document.getElementById('produto_select');
    const option = select.options[select.selectedIndex];
    
    if (option.value) {
        document.getElementById('produto_valor').value = option.dataset.valor || '';
    } else {
        document.getElementById('produto_valor').value = '';
    }
}

// Função para alternar seção de parcelas
function toggleParcelas() {
    const condicoes = document.getElementById('condicoes_pagamento').value;
    const section = document.getElementById('parcelas-section');
    
    if (condicoes === 'Parcelado') {
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
        parcelas = [];
        if (typeof atualizarListaParcelas === 'function') {
            atualizarListaParcelas();
        }
    }
}

// Função para imprimir OS
function imprimirOS() {
    window.print();
}

// Função para validar formulário antes do envio
function validarFormulario() {
    const clienteId = document.getElementById('cliente_id').value;
    
    if (!clienteId) {
        alert('Por favor, selecione um cliente');
        document.getElementById('cliente_id').focus();
        return false;
    }
    
    return true;
}

// Event listener para o formulário
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-os');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Preparar dados JSON para envio
            const servicosInput = document.getElementById('servicos_json');
            const produtosInput = document.getElementById('produtos_json');
            const parcelasInput = document.getElementById('parcelas_json');
            
            if (servicosInput) servicosInput.value = JSON.stringify(servicos || []);
            if (produtosInput) produtosInput.value = JSON.stringify(produtos || []);
            if (parcelasInput) parcelasInput.value = JSON.stringify(parcelas || []);
        });
    }
    
    // Event listeners para campos específicos
    const clienteSelect = document.getElementById('cliente_id');
    if (clienteSelect) {
        clienteSelect.addEventListener('change', preencherDadosCliente);
    }
    
    const produtoSelect = document.getElementById('produto_select');
    if (produtoSelect) {
        produtoSelect.addEventListener('change', preencherValorProduto);
    }
    
    const kmInicial = document.getElementById('km_inicial');
    if (kmInicial) {
        kmInicial.addEventListener('input', calcularDeslocamento);
    }
    
    const kmFinal = document.getElementById('km_final');
    if (kmFinal) {
        kmFinal.addEventListener('input', calcularDeslocamento);
    }
    
    const horaInicio = document.getElementById('hora_inicio');
    if (horaInicio) {
        horaInicio.addEventListener('change', calcularHoras);
    }
    
    const horaTermino = document.getElementById('hora_termino');
    if (horaTermino) {
        horaTermino.addEventListener('change', calcularHoras);
    }
    
    const condicoesPagamento = document.getElementById('condicoes_pagamento');
    if (condicoesPagamento) {
        condicoesPagamento.addEventListener('change', toggleParcelas);
    }
    
    // Inicializar totais
    if (typeof calcularTotais === 'function') {
        calcularTotais();
    }
});

// Exportar funções para uso global
window.preencherDadosCliente = preencherDadosCliente;
window.preencherValorProduto = preencherValorProduto;
window.toggleParcelas = toggleParcelas;
window.imprimirOS = imprimirOS;
window.validarFormulario = validarFormulario;

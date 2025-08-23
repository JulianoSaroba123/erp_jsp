/**
 * Fallback JavaScript for Cliente functionality
 * Provides essential functionality when jQuery fails to load from CDN
 */

// Simple jQuery-like selector function
function $(selector) {
    if (typeof selector === 'string') {
        return document.querySelector(selector);
    }
    return selector;
}

// Add basic event handling
function addEvent(element, event, handler) {
    if (element.addEventListener) {
        element.addEventListener(event, handler);
    } else if (element.attachEvent) {
        element.attachEvent('on' + event, handler);
    }
}

// Simple mask function for CPF/CNPJ
function applyMask(input, mask) {
    if (!input) return;
    
    addEvent(input, 'input', function() {
        let value = this.value.replace(/\D/g, '');
        let masked = '';
        
        if (mask === 'cpf') {
            // 000.000.000-00
            if (value.length > 0) masked += value.substring(0, 3);
            if (value.length > 3) masked += '.' + value.substring(3, 6);
            if (value.length > 6) masked += '.' + value.substring(6, 9);
            if (value.length > 9) masked += '-' + value.substring(9, 11);
        } else if (mask === 'cnpj') {
            // 00.000.000/0000-00
            if (value.length > 0) masked += value.substring(0, 2);
            if (value.length > 2) masked += '.' + value.substring(2, 5);
            if (value.length > 5) masked += '.' + value.substring(5, 8);
            if (value.length > 8) masked += '/' + value.substring(8, 12);
            if (value.length > 12) masked += '-' + value.substring(12, 14);
        } else if (mask === 'phone') {
            // (00) 00000-0000
            if (value.length > 0) masked += '(' + value.substring(0, 2);
            if (value.length > 2) masked += ') ' + value.substring(2, 7);
            if (value.length > 7) masked += '-' + value.substring(7, 11);
        } else if (mask === 'cep') {
            // 00000-000
            if (value.length > 0) masked += value.substring(0, 5);
            if (value.length > 5) masked += '-' + value.substring(5, 8);
        }
        
        this.value = masked;
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Cliente fallback script loaded');
    
    // Get form elements
    var cpfCnpjInput = $('#cpf_cnpj');
    var telefoneInput = $('#telefone');
    var cepInput = $('#cep');
    var tipoPessoaInputs = document.querySelectorAll('input[name="tipo_pessoa"]');
    
    // Apply masks
    if (telefoneInput) applyMask(telefoneInput, 'phone');
    if (cepInput) applyMask(cepInput, 'cep');
    
    // Handle person type change
    function updatePersonType() {
        var isChecked = false;
        var checkedValue = '';
        
        for (var i = 0; i < tipoPessoaInputs.length; i++) {
            if (tipoPessoaInputs[i].checked) {
                isChecked = true;
                checkedValue = tipoPessoaInputs[i].value;
                break;
            }
        }
        
        if (isChecked && cpfCnpjInput) {
            if (checkedValue === 'PF') {
                applyMask(cpfCnpjInput, 'cpf');
                var label = $('#label_cpf_cnpj');
                if (label) label.textContent = 'CPF *';
                var hint = $('#hint_cpf_cnpj');
                if (hint) hint.textContent = 'Digite apenas números do CPF';
                
                // Hide fields for PF
                var nomeFantasia = $('#nome_fantasia');
                var inscricaoEstadual = $('#inscricao_estadual');
                var inscricaoMunicipal = $('#inscricao_municipal');
                
                if (nomeFantasia && nomeFantasia.closest) {
                    var container = nomeFantasia.closest('.col-md-6');
                    if (container) container.style.display = 'none';
                }
                if (inscricaoEstadual && inscricaoEstadual.closest) {
                    var container = inscricaoEstadual.closest('.col-md-6');
                    if (container) container.style.display = 'none';
                }
                if (inscricaoMunicipal && inscricaoMunicipal.closest) {
                    var container = inscricaoMunicipal.closest('.col-md-6');
                    if (container) container.style.display = 'none';
                }
            } else if (checkedValue === 'PJ') {
                applyMask(cpfCnpjInput, 'cnpj');
                var label = $('#label_cpf_cnpj');
                if (label) label.textContent = 'CNPJ *';
                var hint = $('#hint_cpf_cnpj');
                if (hint) hint.textContent = 'Digite apenas números do CNPJ';
                
                // Show fields for PJ
                var nomeFantasia = $('#nome_fantasia');
                var inscricaoEstadual = $('#inscricao_estadual');
                var inscricaoMunicipal = $('#inscricao_municipal');
                
                if (nomeFantasia && nomeFantasia.closest) {
                    var container = nomeFantasia.closest('.col-md-6');
                    if (container) container.style.display = 'block';
                }
                if (inscricaoEstadual && inscricaoEstadual.closest) {
                    var container = inscricaoEstadual.closest('.col-md-6');
                    if (container) container.style.display = 'block';
                }
                if (inscricaoMunicipal && inscricaoMunicipal.closest) {
                    var container = inscricaoMunicipal.closest('.col-md-6');
                    if (container) container.style.display = 'block';
                }
            }
            
            // Clear and focus on input
            if (cpfCnpjInput) {
                cpfCnpjInput.value = '';
                cpfCnpjInput.focus();
            }
        }
    }
    
    // Add event listeners for person type change
    for (var i = 0; i < tipoPessoaInputs.length; i++) {
        addEvent(tipoPessoaInputs[i], 'change', updatePersonType);
    }
    
    // Initialize person type on page load
    updatePersonType();
    
    // Form validation
    var form = document.querySelector('form');
    if (form) {
        addEvent(form, 'submit', function(e) {
            var nome = $('#nome');
            var cpfCnpj = $('#cpf_cnpj');
            var telefone = $('#telefone');
            
            var nomeValue = nome ? nome.value.trim() : '';
            var cpfCnpjValue = cpfCnpj ? cpfCnpj.value.trim() : '';
            var telefoneValue = telefone ? telefone.value.trim() : '';
            
            if (!nomeValue) {
                alert('Nome é obrigatório!');
                if (nome) nome.focus();
                e.preventDefault();
                return false;
            }
            
            if (!cpfCnpjValue) {
                alert('CPF/CNPJ é obrigatório!');
                if (cpfCnpj) cpfCnpj.focus();
                e.preventDefault();
                return false;
            }
            
            if (!telefoneValue) {
                alert('Telefone é obrigatório!');
                if (telefone) telefone.focus();
                e.preventDefault();
                return false;
            }
        });
    }
});
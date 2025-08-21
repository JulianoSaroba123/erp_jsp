// autocomplete_cliente.js - Autocomplete para campo de cliente na OS
$(document).ready(function() {
  if ($('#cliente_id').length) {
    $('#cliente_id').select2({
      theme: 'bootstrap4',
      placeholder: 'Digite nome, CPF ou CNPJ',
      minimumInputLength: 2,
      ajax: {
        url: '/clientes/api/busca',
        dataType: 'json',
        delay: 250,
        data: function(params) {
          return { q: params.term };
        },
        processResults: function(data) {
          return {
            results: data.map(function(c) {
              return {
                id: c.id,
                text: c.nome + (c.cpf_cnpj ? ' (' + c.cpf_cnpj + ')' : ''),
                cliente: c
              };
            })
          };
        },
        cache: true
      },
      templateResult: function(item) {
        if (!item.id) return item.text;
        return '<b>' + item.text + '</b><br><small>' + (item.cliente.email || '') + ' ' + (item.cliente.telefone || '') + '</small>';
      },
      templateSelection: function(item) {
        return item.text || item.nome;
      },
      escapeMarkup: function(m) { return m; }
    });

    $('#cliente_id').on('select2:select', function(e) {
      var c = e.params.data.cliente;
      // Garante que o <select> terá um <option> real selecionado para o submit
      var select = $('#cliente_id');
      var opt = select.find('option[value="' + c.id + '"]');
      if (opt.length === 0) {
        opt = $('<option>')
          .val(c.id)
          .text(c.nome + (c.cpf_cnpj ? ' (' + c.cpf_cnpj + ')' : ''))
          .attr('selected', 'selected');
        select.append(opt);
      } else {
        opt.prop('selected', true);
      }
      select.val(c.id).trigger('change.select2');
      $('#cpf').val(c.cpf_cnpj || '');
      $('#telefone').val(c.telefone || '');
      $('#email').val(c.email || '');
      $('#endereco').val(c.endereco || '');
    });
  }

  // Garante que o valor do select será enviado no submit
  $('#form-os').on('submit', function(e) {
    var select = $('#cliente_id');
    var val = select.val();
    // Força criação do option real
    if (val && select.find('option[value="' + val + '"]').length === 0) {
      var text = select.select2('data')[0]?.text || '';
      var opt = $('<option>')
        .val(val)
        .text(text)
        .attr('selected', 'selected');
      select.append(opt);
    }
    // Log para depuração
    console.log('SUBMIT: cliente_id =', val, 'options:', select.html());
    if (!val) {
      alert('Selecione um cliente antes de salvar!');
      e.preventDefault();
      return false;
    }
  });
});

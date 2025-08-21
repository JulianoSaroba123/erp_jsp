# 💡 Contexto para GitHub Copilot - Projeto ERP JSP

Você está colaborando no sistema ERP chamado **JSP - Elétrica Industrial**, da empresa **Elétrica Saroba & Solar**.

Siga **rigorosamente** o padrão estabelecido no documento `📘 Padrão Oficial de Desenvolvimento - versão v1.0`.

## 🎯 Diretrizes que você deve seguir:

✅ Use Blueprints para rotas. Nunca defina rotas direto no `app.py`.

✅ Cada módulo (cliente, produto, fornecedor, OS, etc.) deve conter:
- `*_model.py` para models
- `*_routes.py` para rotas
- `templates/<modulo>/` com `cadastro.html`, `lista.html`, etc.

✅ Os templates **devem herdar de `base.html`** e usar o bloco `{% block conteudo %}`.

✅ Inputs devem ter máscaras para CPF/CNPJ, telefone, CEP.

✅ Marque campos obrigatórios com `nullable=False` no Model.

✅ Use código automático nos cadastros: `CLI0001`, `PRD0001`, etc.

✅ Utilize `render_template()` com caminhos corretos e HTMLs padronizados.

✅ Use os seguintes serviços:
- Busca automática de **CEP** com ViaCEP
- Busca automática de **CNPJ** com BrasilAPI

✅ Produto deve ter **cálculo de markup** automático no formulário (JS ou backend).

## 🚫 O que evitar:
- ❌ Não criar pastas novas fora do padrão sem aprovação
- ❌ Não usar funções fictícias (`set_models`, `setup_blueprints`, etc.)
- ❌ Não misturar lógica de negócio com HTML
- ❌ Não colocar lógica de banco de dados em arquivos de rota
'
## 📦 Boas práticas:
- Código limpo, comentado e modular
- Rotas com nomes descritivos como `listar_clientes()`
- Teste local antes de sugerir alterações

## 📂 Estrutura do projeto:
```plaintext
ERP_JSP/
├── app/
│   ├── cliente/
│   ├── fornecedor/
│   ├── produto/
│   ├── ordem_servico/
│   ├── servico/
├── templates/
│   ├── base.html
│   └── index.html

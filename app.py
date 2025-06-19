8from flask import Flask, render_template, request, redirect, send_file, session, url_for
from models import db
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from models.cliente_model import Cliente
from models.produto_model import Produto
from models.produto_model import Produto
from models.servico_model import Servico
from models.fornecedor_model import Fornecedor


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave-secreta-jsp'  # Necessário para sessões

db.init_app(app)

with app.app_context():
    db.create_all()

# Middleware de proteção
@app.before_request
def proteger_rotas():
    rotas_livres = ['login']
    if 'usuario' not in session and request.endpoint not in rotas_livres:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '123':
            session['usuario'] = usuario
            return redirect('/')
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/login')

@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        cliente = Cliente(
            codigo=request.form['codigo'],
            nome=request.form['nome'],
            cpf_cnpj=request.form['cpf_cnpj'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            endereco=request.form['endereco'],
            numero=request.form['numero']
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect('/')
    return render_template('cadastro_cliente.html', cliente=None)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.codigo = request.form['codigo']
        cliente.nome = request.form['nome']
        cliente.cpf_cnpj = request.form['cpf_cnpj']
        cliente.telefone = request.form['telefone']
        cliente.email = request.form['email']
        cliente.endereco = request.form['endereco']
        cliente.numero = request.form['numero']
        db.session.commit()
        return redirect('/')

    return render_template('cadastro_cliente.html', cliente=cliente)

@app.route('/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect('/')
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('lista_produtos.html', produtos=produtos)

from datetime import datetime  # certifique-se de ter essa importação no topo

@app.route('/produto/novo', methods=['GET', 'POST'])
@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_produto(id=None):
    produto = Produto.query.get(id) if id else None

    if request.method == 'POST':
        data = request.form.to_dict()

        try:
            # Conversões seguras dos campos numéricos e de data
            data['valor_venda'] = float(data.get('valor_venda', 0))
            data['valor_compra'] = float(data.get('valor_compra', 0))
            data['estoque'] = int(data.get('estoque', 0))
            data['lucro'] = float(data.get('lucro', 0))
            data['data'] = datetime.strptime(data.get('data', ''), "%Y-%m-%d").date()
        except (ValueError, TypeError) as e:
            return f"Erro ao converter valores numéricos ou data: {e}"

        if produto:
            for key, value in data.items():
                setattr(produto, key, value)
        else:
            produto = Produto(**data)
            db.session.add(produto)

        db.session.commit()
        return redirect('/produtos')

    return render_template('cadastro_produto.html', produto=produto)


@app.route('/produto/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/produtos')
import pandas as pd
from fpdf import FPDF
from datetime import datetime

@app.route('/produtos/exportar_excel')
def exportar_produtos_excel():
    produtos = Produto.query.all()
    dados = [{
        'Nome': p.nome,
        'Código de Barras': p.codigo_barras,
        'Fornecedor': p.fornecedor,
        'Unidade': p.unidade,
        'Valor Venda': p.valor_venda,
        'Valor Compra': p.valor_compra,
        'Estoque': p.estoque,
        'Lucro (%)': p.lucro,
        'Classificação': p.classificacao,
        'Fabricante': p.fabricante,
        'Situação': p.situacao
    } for p in produtos]

    df = pd.DataFrame(dados)
    nome_arquivo = f"produtos_JSP_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    df.to_excel(nome_arquivo, index=False)

    return send_file(nome_arquivo, as_attachment=True)

@app.route('/produtos/exportar_pdf')
def exportar_produtos_pdf():
    produtos = Produto.query.all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Lista de Produtos - ERP JSP", ln=True, align='C')
    pdf.ln(5)

    for p in produtos:
        texto = f"{p.nome} | {p.codigo_barras or ''} | R$ {p.valor_venda:.2f} | Estoque: {p.estoque}"
        pdf.multi_cell(0, 10, texto)
        pdf.ln(1)

    nome_arquivo = f"produtos_JSP_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdf.output(nome_arquivo)
    return send_file(nome_arquivo, as_attachment=True)
    
@app.route('/servicos')
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('lista_servicos.html', servicos=servicos)

@app.route('/servico/novo', methods=['GET', 'POST'])
@app.route('/servico/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_servico(id=None):
    servico = Servico.query.get(id) if id else None

    if request.method == 'POST':
        data = request.form.to_dict()
        data['valor'] = float(data.get('valor', 0.0))

        if servico:
            for key, value in data.items():
                setattr(servico, key, value)
        else:
            servico = Servico(**data)
            db.session.add(servico)

        db.session.commit()
        return redirect('/servicos')

    return render_template('cadastro_servico.html', servico=servico)

@app.route('/servico/excluir/<int:id>')
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return redirect('/servicos')

@app.route('/fornecedores')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('lista_fornecedores.html', fornecedores=fornecedores)

@app.route('/fornecedor/novo', methods=['GET', 'POST'])
@app.route('/fornecedor/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_fornecedor(id=None):
    fornecedor = Fornecedor.query.get(id) if id else None

    if request.method == 'POST':
        data = request.form.to_dict()
        if fornecedor:
            for key, value in data.items():
                setattr(fornecedor, key, value)
        else:
            fornecedor = Fornecedor(**data)
            db.session.add(fornecedor)
        db.session.commit()
        return redirect('/fornecedores')
    return render_template('cadastro_fornecedor.html', fornecedor=fornecedor)

@app.route('/fornecedor/excluir/<int:id>')
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect('/fornecedores')
@app.route('/exportar_excel')
def exportar_excel():
    clientes = Cliente.query.all()

    dados = [{
        'Código': c.codigo,
        'Nome': c.nome,
        'CPF/CNPJ': c.cpf_cnpj,
        'Telefone': c.telefone,
        'Email': c.email,
        'Endereço': f'{c.endereco}, Nº {c.numero}'
    } for c in clientes]

    df = pd.DataFrame(dados)
    caminho = 'clientes_exportados.xlsx'
    df.to_excel(caminho, index=False)

    nome_arquivo = f"Clientes_JSP_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    return send_file(caminho, as_attachment=True, download_name=nome_arquivo)

@app.route('/exportar_pdf')
def exportar_pdf():
    clientes = Cliente.query.all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Lista de Clientes - ERP JSP", ln=True, align='C')
    pdf.ln(10)

    for c in clientes:
        texto = f"{c.codigo or ''} - {c.nome} | {c.cpf_cnpj} | {c.telefone} | {c.email} | {c.endereco}, Nº {c.numero}"
        pdf.multi_cell(0, 10, texto)
        pdf.ln(1)

    caminho = "clientes_exportados.pdf"
    pdf.output(caminho)

    nome_arquivo = f"Clientes_JSP_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    return send_file(caminho, as_attachment=True, download_name=nome_arquivo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


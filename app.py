# app.py
from flask import Flask, render_template, request, redirect, send_file, session, url_for
from models import db
from models.cliente_model import Cliente
from models.produto_model import Produto
from models.servico_model import Servico
from models.fornecedor_model import Fornecedor
from models.os_model import OrdemServico
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from flask import jsonify

# Função para gerar códigos automáticos com prefixo (ex: CLT00001)
def gerar_codigo(model, prefixo, inicio=1):
    ultimo = model.query.order_by(model.id.desc()).first()
    if ultimo and ultimo.codigo and ultimo.codigo.startswith(prefixo):
        try:
            num = int(ultimo.codigo.replace(prefixo, ''))
        except:
            num = inicio
        novo_num = num + 1
    else:
        novo_num = inicio
    return f"{prefixo}{novo_num:05d}"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave-secreta-jsp'

db.init_app(app)

with app.app_context():
    db.create_all()

# Proteção de rotas
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

# --- CLIENTES ---
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        codigo = gerar_codigo(Cliente, 'CLT')
    else:
         codigo = gerar_codigo(Cliente, 'CLT')
    return redirect('/')
return
render_template('cadastro_cliente.html',
        cliente = None, codigo=codigo)
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

# --- PRODUTOS ---
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('lista_produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_produto(id=None):
    from datetime import datetime
    produto = Produto.query.get(id) if id else None
    fornecedores = Fornecedor.query.all()  # Pega fornecedores para o select

    if request.method == 'POST':
        data = request.form.to_dict()
        # Conversão correta da data
        data_str = data.get('data', '')
        if data_str:
            try:
                data['data'] = datetime.strptime(data_str, "%Y-%m-%d").date()
            except Exception:
                return "Data em formato inválido. Use o formato AAAA-MM-DD."
        else:
            data['data'] = None

        data['valor_venda'] = float(data.get('valor_venda', 0))
        data['valor_compra'] = float(data.get('valor_compra', 0)) 
        data['estoque'] = int(data.get('estoque', 0))
        data['lucro'] = float(data.get('lucro', 0))

        if produto:
            for key, value in data.items():
                setattr(produto, key, value)
        else:
            # Geração de código automático
            data['codigo'] = gerar_codigo(Produto, prefixo='PRD')
            produto = Produto(**data)
            db.session.add(produto)

        db.session.commit()
        return redirect('/produtos')

    return render_template('cadastro_produto.html', produto=produto, fornecedores=fornecedores)

    produto = Produto.query.get(id) if id else None
    if request.method == 'POST':
        if not produto:
            codigo = gerar_codigo(Produto, 'PRD')
            produto = Produto(codigo=codigo)
            db.session.add(produto)
        produto.nome = request.form['nome']
        produto.codigo_barras = request.form['codigo_barras']
        produto.data = request.form['data']
        produto.fornecedor = request.form['fornecedor']
        produto.unidade = request.form['unidade']
        produto.classificacao = request.form['classificacao']
        produto.localizacao = request.form['localizacao']
        produto.situacao = request.form['situacao']
        produto.valor_venda = float(request.form['valor_venda'])
        produto.valor_compra = float(request.form['valor_compra'])
        produto.estoque = int(request.form['estoque'])
        produto.lucro = float(request.form['lucro'])
        produto.fabricante = request.form['fabricante']
        produto.numero_serie = request.form['numero_serie']
        db.session.commit()
        return redirect('/produtos')
    return render_template('cadastro_produto.html', produto=produto)

@app.route('/produto/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/produtos')

# --- SERVIÇOS ---
@app.route('/servicos')
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('lista_servicos.html', servicos=servicos)

@app.route('/servico/novo', methods=['GET', 'POST'])
@app.route('/servico/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_servico(id=None):
    servico = Servico.query.get(id) if id else None
    if request.method == 'POST':
        if not servico:
            codigo = gerar_codigo(Servico, 'SRV')
            servico = Servico(codigo=codigo)
            db.session.add(servico)
        servico.nome = request.form['nome']
        servico.valor = float(request.form['valor'])
        servico.unidade = request.form['unidade']
        servico.situacao = request.form['situacao']
        db.session.commit()
        return redirect('/servicos')
    return render_template('cadastro_servico.html', servico=servico)

@app.route('/servico/excluir/<int:id>')
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return redirect('/servicos')

# --- FORNECEDORES ---
@app.route('/fornecedores')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('lista_fornecedores.html', fornecedores=fornecedores)

@app.route('/fornecedor/novo', methods=['GET', 'POST'])
@app.route('/fornecedor/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_fornecedor(id=None):
    fornecedor = Fornecedor.query.get(id) if id else None
    if request.method == 'POST':
        if not fornecedor:
            codigo = gerar_codigo(Fornecedor, 'FRN')
            fornecedor = Fornecedor(codigo=codigo)
            db.session.add(fornecedor)
        fornecedor.nome = request.form['nome']
        fornecedor.cnpj = request.form['cnpj']
        fornecedor.telefone = request.form['telefone']
        fornecedor.cep = request.form['cep']
        fornecedor.cidade = request.form['cidade']
        fornecedor.endereco = request.form['endereco']
        db.session.commit()
        return redirect('/fornecedores')
    return render_template('cadastro_fornecedor.html', fornecedor=fornecedor)

@app.route('/fornecedor/excluir/<int:id>')
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect('/fornecedores')

# --- ORDEM DE SERVIÇO (EXEMPLO SIMPLES) ---
@app.route('/ordens_servico')
def lista_ordens_servico():
    ordens = OrdemServico.query.all()
    return render_template('lista_ordens_servico.html', ordens=ordens)

@app.route('/ordem_servico/novo', methods=['GET', 'POST'])
@app.route('/ordem_servico/editar/<int:id>', methods=['GET', 'POST'])
def cadastro_ordem_servico(id=None):
    os = OrdemServico.query.get(id) if id else None
    if request.method == 'POST':
        if not os:
            codigo = gerar_codigo(OrdemServico, 'OSV')
            os = OrdemServico(codigo=codigo)
            db.session.add(os)
        # Adapte aqui conforme seus campos de OS
        os.cliente_id = request.form['cliente_id']
        os.descricao = request.form['descricao']
        os.data_emissao = datetime.strptime(request.form['data_emissao'], "%Y-%m-%d")
        db.session.commit()
        return redirect('/ordens_servico')
    return render_template('cadastro_ordem_servico.html', os=os)

@app.route('/ordem_servico/excluir/<int:id>')
def excluir_ordem_servico(id):
    os = OrdemServico.query.get_or_404(id)
    db.session.delete(os)
    db.session.commit()
    return redirect('/ordens_servico')
    # --- AUTOCOMPLETE CLIENTE ---
@app.route('/buscar_clientes')
def buscar_clientes():
    termo = request.args.get('q', '')
    clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "cpf_cnpj": c.cpf_cnpj,
            "telefone": c.telefone,
            "email": c.email,
            "endereco": c.endereco
        } for c in clientes
    ])

# --- AUTOCOMPLETE PRODUTO ---
@app.route('/buscar_produtos')
def buscar_produtos():
    termo = request.args.get('q', '')
    produtos = Produto.query.filter(Produto.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "valor_venda": p.valor_venda
        } for p in produtos
    ])
    # --- AUTOCOMPLETE SERVIÇOS ---
@app.route('/buscar_servicos')
def buscar_servicos():
    termo = request.args.get('q', '')
    servicos = Servico.query.filter(Servico.nome.ilike(f'%{termo}%')).all()
    lista = []
    for s in servicos:
        lista.append({
            'id': s.id,
            'nome': s.nome,
            'descricao': s.descricao,
            'valor': float(s.valor)
        })
    return jsonify(lista)
# --- EXPORTAÇÕES CLIENTE/PRODUTO/OS ---
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
    nome_arquivo = f"Clientes_JSP_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    df.to_excel(nome_arquivo, index=False)
    return send_file(nome_arquivo, as_attachment=True, download_name=nome_arquivo)

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

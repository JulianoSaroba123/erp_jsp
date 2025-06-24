from flask import Flask, render_template, request, redirect, send_file, session, url_for, jsonify
from models import db
from models.cliente_model import Cliente
from models.produto_model import Produto
from models.servico_model import Servico
from models.fornecedor_model import Fornecedor
from models.os_model import OrdemServico
from models.tipo_servico_model import TipoServico
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Função para gerar códigos automáticos (CLT/PRD/SRV/FRN/OSV)
def gerar_codigo(model, prefixo, inicio=1):
    ultimo = model.query.order_by(model.id.desc()).first()
    if ultimo and ultimo.codigo and ultimo.codigo.startswith(prefixo):
        try:
            num = int(ultimo.codigo.replace(prefixo, ''))
        except Exception:
            num = inicio
        novo_num = num + 1
    else:
        novo_num = inicio
    return f"{prefixo}{novo_num:05d}"

# Configuração Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://erp_jsp_db_user:gdFfYSCkyJG20d13hZl301mEZ63QZH18@dpg-d1d1f3fdiees73ccik6g-a.oregon-postgres.render.com/erp_jsp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave-secreta-jsp'
db.init_app(app)

with app.app_context():
    db.create_all()

# Proteção de Rotas
@app.before_request
def proteger_rotas():
    rotas_livres = ['login', 'static']
    if 'usuario' not in session and request.endpoint not in rotas_livres:
        return redirect(url_for('login'))

# LOGIN
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

# CLIENTES
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        codigo = gerar_codigo(Cliente, 'CLT')
        cliente = Cliente(
            codigo=codigo,
            nome=request.form['nome'],
            cpf_cnpj=request.form['cnpj_cpf'],
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
        cliente.cpf_cnpj = request.form['cnpj_cpf']
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

# PRODUTOS
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('lista_produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_produto(id=None):
    produto = Produto.query.get(id) if id else None
    fornecedores = Fornecedor.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['data'] = None
        if data.get('data', ''):
            try:
                data['data'] = datetime.strptime(data['data'], "%Y-%m-%d").date()
            except:
                data['data'] = None
        data['valor_venda'] = float(data.get('valor_venda', 0))
        data['valor_compra'] = float(data.get('valor_compra', 0))
        data['estoque'] = int(data.get('estoque', 0))
        data['lucro'] = float(data.get('lucro', 0))
        if produto:
            for key, value in data.items():
                setattr(produto, key, value)
        else:
            data['codigo'] = gerar_codigo(Produto, 'PRD')
            produto = Produto(**data)
            db.session.add(produto)
        db.session.commit()
        return redirect('/produtos')
    return render_template('cadastro_produto.html', produto=produto, fornecedores=fornecedores)

@app.route('/produto/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/produtos')

# SERVIÇOS
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

# FORNECEDORES
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

# ORDEM DE SERVIÇO
@app.route('/ordens_servico')
def lista_ordens_servico():
    ordens = OrdemServico.query.all()
    return render_template('lista_ordens_servico.html', ordens=ordens)

@app.route('/ordem_servico/novo', methods=['GET', 'POST'])
@app.route('/ordem_servico/editar/<int:id>', methods=['GET', 'POST'])
def cadastro_ordem_servico(id=None):
    tipos_servico = TipoServico.query.all() #<- Coloquei essa linha Agora de pouco
    os = OrdemServico.query.get(id) if id else None
    if request.method == 'POST':
        if not os:
            codigo = gerar_codigo(OrdemServico, 'OSV')
            os = OrdemServico(codigo=codigo)
            db.session.add(os)
        os.cliente_nome = request.form.get('cliente_nome')
        os.cliente_cnpj_cpf = request.form.get('cliente_cnpj_cpf')
        os.cliente_telefone = request.form.get('cliente_telefone')
        os.cliente_email = request.form.get('cliente_email')
        os.cliente_endereco = request.form.get('cliente_endereco')
        os.data_emissao = request.form.get('data_emissao')
        os.previsao_conclusao = request.form.get('previsao_conclusao')
        os.tipo_servico = request.form.get('tipo_servico')
        os.descricao_servico = request.form.get('descricao_servico')
        os.produtos = request.form.get('produtos')
        os.tecnico_responsavel = request.form.get('tecnico_responsavel')
        os.hora_inicio = request.form.get('hora_inicio')
        os.hora_termino = request.form.get('hora_termino')
        os.total_horas = request.form.get('total_horas')
        os.atividade_realizada = request.form.get('atividade_realizada')
        os.km_inicial = request.form.get('km_inicial')
        os.km_final = request.form.get('km_final')
        os.km_total = request.form.get('km_total')
        os.valor_servicos = request.form.get('valor_servicos')
        os.valor_produtos = request.form.get('valor_produtos')
        os.valor_deslocamento = request.form.get('valor_deslocamento')
        os.total_geral = request.form.get('total_geral')
        os.condicoes_pagamento = request.form.get('condicoes_pagamento')
        os.observacoes = request.form.get('observacoes')
        db.session.commit()
        return redirect('/ordens_servico')
    return render_template('cadastro_ordem_servico.html', os=os, tipos_servico=tipos_servico)

@app.route('/ordem_servico/excluir/<int:id>')
def excluir_ordem_servico(id):
    os = OrdemServico.query.get_or_404(id)
    db.session.delete(os)
    db.session.commit()
    return redirect('/ordens_servico')

# AUTOCOMPLETE E BUSCAS
@app.route('/buscar_clientes')
def buscar_clientes():
    termo = request.args.get('q', '')
    clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "cpf_cnpj": c.cnpj_cpf,
            "telefone": c.telefone,
            "email": c.email,
            "endereco": c.endereco
        } for c in clientes
    ])

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

@app.route('/buscar_servicos')
def buscar_servicos():
    termo = request.args.get('q', '')
    servicos = Servico.query.filter(Servico.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {
            "id": s.id,
            "nome": s.nome,
            "descricao": getattr(s, 'descricao', ''),
            "valor": float(s.valor)
        } for s in servicos
    ])

@app.route('/buscar_tipos_servico')
def buscar_tipos_servico():
    termos = TipoServico.query.all()
    return jsonify([{'id': t.id, 'text': t.nome} for t in termos])

@app.route('/adicionar_tipo_servico', methods=['POST'])
def adicionar_tipo_servico():
    nome = request.form.get('nome')
    if not nome:
        return jsonify({'success': False})
    nome = nome.strip().lower()    
    tipo = TipoServico.query.filter_by(nome=nome).first()
    if not tipo:
        tipo = TipoServico(nome=nome)
        db.session.add(tipo)
        db.session.commit()
    return jsonify({'id': tipo.id, 'text': tipo.nome})

@app.route('/cadastrar_tipo_servico')
def cadastrar_tipo_servico():
    tipos = ['Manutenção', 'Instalação', 'Laudo', 'Outros']
    for t in tipos:
        if not TipoServico.query.filter_by(nome=t).first():
            db.session.add(TipoServico(nome=t))
    db.session.commit()
    return "Tipos de serviço cadastrados"
    from models.tipo_servico_model import TipoServico

@app.route('/tipos_servico')
def lista_tipos_servico():
    tipos = TipoServico.query.all()
    return render_template('lista_tipos_servico.html', tipos=tipos)

@app.route('/tipo_servico/novo', methods=['GET', 'POST'])
@app.route('/tipo_servico/editar/<int:id>', methods=['GET', 'POST'])
@app.route('/tipo_servico/excluir/<int:id>')
def excluir_tipo_servico(id):
    tipo = TipoServico.query.get(id)
    if tipo:
        db.session.delete(tipo)
        db.session.commit()
    return redirect('/tipos_servico')  
def cadastro_tipo_servico(id=None):
    tipo = TipoServico.query.get(id) if id else None
    if request.method == 'POST':
        nome = request.form['nome']
        if not tipo:
            tipo = TipoServico(nome=nome)
            db.session.add(tipo)
        else:
            tipo.nome = nome
        db.session.commit()
        return redirect('/tipos_servico')
    return render_template('cadastro_tipo_servico.html', tipo=tipo)
    
   
# EXPORTAÇÃO
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

# RODAR SERVIDOR
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

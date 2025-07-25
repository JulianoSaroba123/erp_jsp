from flask import Flask, render_template, request, redirect, send_file, session, url_for, jsonify, make_response
from models import db
from models.cliente_model import Cliente
from models.produto_model import Produto
from models.servico_model import Servico
from models.fornecedor_model import Fornecedor
from models.os_model import OrdemServico
from models.tipo_servico_model import TipoServico
from flask_migrate import Migrate
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import json
import os


# Inicialização do app Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_jsp.db'
if 'RENDER' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_jsp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# Proteção de Rotas
@app.before_request
def proteger_rotas():
    rotas_livres = ['login', 'static']
    if 'usuario' not in session and request.endpoint not in rotas_livres:
        return redirect(url_for('login'))

# Função para gerar códigos
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
    return f"{prefixo}{novo_num:03d}"

def gerar_codigo_os():
    return gerar_codigo(OrdemServico, 'OS')

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

# CLIENTES - Limpar campos
@app.route('/cliente/limpar/<int:id>')
def limpar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.nome = ''
    cliente.cpf_cnpj = ''
    cliente.telefone = ''
    cliente.email = ''
    cliente.endereco = ''
    cliente.numero = ''
    db.session.commit()
    return redirect(url_for('editar', id=cliente.id))

# PRODUTOS
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.filter_by(situacao='Ativo').all()
    return render_template('lista_produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_produto(id=None):
    produto = Produto.query.get(id) if id else None
    fornecedores = Fornecedor.query.all()
    if request.method == 'POST':
        data_form = request.form.to_dict()
        data_produto = {}

        # Gere o código automaticamente se for novo
        if not produto:
            data_produto['codigo'] = gerar_codigo(Produto, 'PRD')

        # Campos obrigatórios (sem descricao)
        data_produto['nome'] = data_form.get('nome', '')
        data_produto['fornecedor_id'] = data_form.get('fornecedor_id')
        data_produto['valor_compra'] = float(data_form.get('valor_compra', 0))
        data_produto['markup_percentual'] = float(data_form.get('markup_percentual', 0))
        data_produto['valor_venda'] = float(data_form.get('valor_venda', 0))
        data_produto['lucro_percentual'] = float(data_form.get('lucro_percentual', 0))
        data_produto['estoque'] = int(data_form.get('estoque', 0))
        data_produto['unidade'] = data_form.get('unidade', '')
       
        data_produto['situacao'] = data_form.get('situacao', 'Ativo')

        # Data (se existir no modelo)
        if 'data' in Produto.__table__.columns:
            data_str = data_form.get('data', '')
            if data_str:
                try:
                    data_produto['data'] = datetime.strptime(data_str, "%Y-%m-%d").date()
                except:
                    data_produto['data'] = None

        if produto:
            for key, value in data_produto.items():
                setattr(produto, key, value)
        else:
            produto = Produto(**data_produto)
            db.session.add(produto)
        db.session.commit()
        return redirect('/produtos')
    return render_template('cadastro_produto.html', produto=produto, fornecedores=fornecedores, codigo_gerado=gerar_codigo(Produto, 'PRD'))

@app.route('/produto/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/produtos')

# PRODUTOS - Limpar campos
@app.route('/produto/limpar/<int:id>')
def limpar_produto(id):
    produto = Produto.query.get_or_404(id)
    produto.nome = ''
    produto.codigo = ''
    produto.valor_compra = 0
    produto.valor_venda = 0
    produto.lucro_percentual = 0
    produto.estoque = 0
    produto.unidade = ''
    
   
    db.session.commit()
    return redirect(url_for('cadastrar_produto', id=produto.id))

# SERVIÇOS
@app.route('/servicos')
def listar_servicos():
    servicos = Servico.query.filter_by(situacao='Ativo').all()
    return render_template('lista_servicos.html', servicos=servicos)

@app.route('/servico/novo', methods=['GET', 'POST'])
@app.route('/servico/editar/<int:id>', methods=['GET', 'POST'])
def cadastrar_servico(id=None):
    servico = Servico.query.get(id) if id else None
    codigo_gerado = gerar_codigo(Servico, 'SRV')
    if request.method == 'POST':
        if not servico:
            servico = Servico(codigo=codigo_gerado)
            db.session.add(servico)
        servico.nome = request.form['nome']
        servico.valor = float(request.form['valor'])
        servico.unidade = request.form['unidade']
        servico.situacao = request.form.get('situacao', 'Ativo')
        db.session.commit()
        return redirect(url_for('listar_servicos'))
    return render_template('cadastro_servico.html', servico=servico, codigo_gerado=codigo_gerado)

@app.route('/servico/excluir/<int:id>')
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return redirect(url_for('listar_servicos'))

@app.route('/servico/limpar/<int:id>')
def limpar_servico(id):
    servico = Servico.query.get_or_404(id)
    servico.nome = ''
    servico.valor = 0
    servico.unidade = ''
    servico.situacao = ''
    db.session.commit()
    return redirect(url_for('cadastrar_servico', id=servico.id))

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

# FORNECEDORES - Limpar campos
@app.route('/fornecedor/limpar/<int:id>')
def limpar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    fornecedor.nome = ''
    fornecedor.cnpj = ''
    fornecedor.telefone = ''
    fornecedor.cep = ''
    fornecedor.cidade = ''
    fornecedor.endereco = ''
    db.session.commit()
    return redirect(url_for('cadastrar_fornecedor', id=fornecedor.id))

# ORDEM DE SERVIÇO

@app.route('/ordens_servico')
def lista_ordens_servico():
    ordens = OrdemServico.query.all()
    # passa os=None para evitar erro de variável indefinida no template
    return render_template('lista_ordens_servico.html', ordens=ordens, os=None)

@app.route('/ordem_servico/novo', methods=['GET', 'POST'])
@app.route('/ordem_servico/editar/<int:id>', methods=['GET', 'POST'])
def cadastro_ordem_servico(id=None):
    # Recupera ou instancia
    os = OrdemServico.query.get(id) if id else None
    # Option lists
    clientes = Cliente.query.all()
    tipos_servico = TipoServico.query.all()
    servicos = Servico.query.all()
    produtos = Produto.query.all()

    # Processa JSON salvos
    servicos_json = []
    produtos_json = []
    parcelas_json = []
    if os:
        try:
            servicos_json = json.loads(os.servicos or '[]')
        except:
            servicos_json = []
        try:
            produtos_json = json.loads(os.produtos or '[]')
        except:
            produtos_json = []
        try:
            parcelas_json = os.parcelas or []
        except:
            parcelas_json = []
    # Garante listas
    servicos_json = servicos_json if isinstance(servicos_json, list) else []
    produtos_json = produtos_json if isinstance(produtos_json, list) else []
    parcelas_json = parcelas_json if isinstance(parcelas_json, list) else []

    if request.method == 'POST':
        # Cria nova OS se necessário
        if not os:
            os = OrdemServico()
            os.codigo = request.form.get('codigo') or gerar_codigo_os()
            db.session.add(os)
        # Campos básicos
        os.cliente_id = request.form.get('cliente_id')
        os.codigo = request.form.get('codigo', os.codigo)
        os.tipo_servico = request.form.get('tipo_servico','')
        # Datas
        d1 = request.form.get('data_emissao')
        d2 = request.form.get('previsao_conclusao')
        os.data_emissao = datetime.strptime(d1,'%Y-%m-%d').date() if d1 else None
        os.previsao_conclusao = datetime.strptime(d2,'%Y-%m-%d').date() if d2 else None
        # Técnico
        os.tecnico = request.form.get('tecnico','')
        # Horários
        os.hora_inicio = request.form.get('hora_inicio','')
        os.hora_termino = request.form.get('hora_termino','')
        os.total_horas = request.form.get('total_horas','')
        # Quilometragem
        os.km_inicial = float(request.form.get('km_inicial') or 0)
        os.km_final = float(request.form.get('km_final') or 0)
        os.km_total = float(request.form.get('km_total') or 0)
        os.valor_deslocamento = float(request.form.get('valor_deslocamento') or 0)
        # Valores
        os.valor_servicos = float(request.form.get('valor_servicos') or 0)
        os.valor_produtos = float(request.form.get('valor_produtos') or 0)
        os.total_geral = float(request.form.get('valor_total') or 0)
        # Observações e Outras
        os.observacoes = request.form.get('observacoes','')
        os.outras_informacoes = request.form.get('outras_informacoes','')
        # Equipamento
        os.equipamento_nome = request.form.get('equipamento_nome','')
        os.equipamento_marca = request.form.get('equipamento_marca','')
        os.equipamento_modelo = request.form.get('equipamento_modelo','')
        os.equipamento_numero_serie = request.form.get('equipamento_numero_serie','')
        os.equipamento_acessorios = request.form.get('equipamento_acessorios','')
        os.problema_descrito = request.form.get('problema_descrito','')
        # Descrição do serviço
        os.descricao_servico_realizado = request.form.get('descricao_servico_realizado','')
        # Condições de pagamento e parcelamento
        os.condicoes_pagamento = request.form.get('condicoes_pagamento','')
        os.pago_parcelado = (os.condicoes_pagamento == 'Parcelado')
        try:
            os.parcelas = json.loads(request.form.get('parcelas_json','[]')) if os.pago_parcelado else []
        except:
            os.parcelas = []
        # Serviços e produtos (listas JSON)
        os.servicos = request.form.get('servicos_json','[]')
        os.produtos = request.form.get('produtos_json','[]')
        tipo_cobranca = request.form.get('tipo_cobranca')
        os.tipo_cobranca = tipo_cobranca

        db.session.commit()
        return redirect(url_for('lista_ordens_servico'))

    # GET → renderiza
    return render_template(
        'cadastro_ordem_servico.html',
        os=os,
        clientes=clientes,
        tipos_servico=tipos_servico,
        servicos=servicos,
        produtos=produtos,
        servicos_salvos=servicos_json,
        produtos_salvos=produtos_json,
        parcelas_salvas=parcelas_json,
        codigo_gerado=gerar_codigo_os()
    )

@app.route('/ordem_servico/excluir/<int:id>', methods=['POST'])
def excluir_ordem_servico(id):
    os = OrdemServico.query.get_or_404(id)
    db.session.delete(os)
    db.session.commit()
    return redirect(url_for('lista_ordens_servico'))

@app.route('/ordem_servico/limpar/<int:id>')
def limpar_ordem_servico(id):
    os = OrdemServico.query.get_or_404(id)
    # Limpa somente campos editáveis
    for field in ['cliente_id','tipo_servico','data_emissao','previsao_conclusao',
                  'tecnico','hora_inicio','hora_termino','total_horas',
                  'km_inicial','km_final','km_total','valor_deslocamento',
                  'valor_servicos','valor_produtos','total_geral',
                  'observacoes','outras_informacoes',
                  'equipamento_nome','equipamento_marca','equipamento_modelo',
                  'equipamento_numero_serie','equipamento_acessorios','problema_descrito',
                  'descricao_servico_realizado','condicoes_pagamento']:
        setattr(os, field, None)
    os.parcelas = []
    os.servicos = '[]'
    os.produtos = '[]'
    db.session.commit()
    return redirect(url_for('cadastro_ordem_servico', id=os.id))



# AUTOCOMPLETE E BUSCAS
@app.route('/buscar_clientes')
def buscar_clientes():
    termo = request.args.get('q', '')
    clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {"id": c.id, "nome": c.nome, "cpf_cnpj": c.cpf_cnpj, "telefone": c.telefone, "email": c.email, "endereco": c.endereco}
        for c in clientes
    ])

@app.route('/buscar_produtos')
def buscar_produtos():
    termo = request.args.get('q', '')
    produtos = Produto.query.filter(Produto.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {"id": p.id, "nome": p.nome, "valor_venda": p.valor_venda}
        for p in produtos
    ])

@app.route('/buscar_servicos')
def buscar_servicos():
    termo = request.args.get('q', '')
    servicos = Servico.query.filter(Servico.nome.ilike(f'%{termo}%')).all()
    return jsonify([
        {"id": s.id, "nome": s.nome, "descricao": getattr(s, 'descricao', ''), "valor": float(s.valor)}
        for s in servicos
    ])

@app.route('/buscar_tipos_servico')
def buscar_tipos_servico():
    termos = TipoServico.query.all()
    return jsonify([{'id': t.id, 'text': t.nome} for t in termos])

# CRUD Tipos de Serviço
@app.route('/tipos_servico')
def lista_tipos_servico():
    tipos = TipoServico.query.all()
    return render_template('lista_tipos_servico.html', tipos=tipos)

@app.route('/tipo_servico/novo', methods=['GET', 'POST'])
@app.route('/tipo_servico/editar/<int:id>', methods=['GET', 'POST'])
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

@app.route('/tipo_servico/excluir/<int:id>')
def excluir_tipo_servico(id):
    tipo = TipoServico.query.get(id)
    if tipo:
        db.session.delete(tipo)
        db.session.commit()
    return redirect('/tipos_servico')

@app.route('/tipo_servico/limpar/<int:id>')
def limpar_tipo_servico(id):
    tipo = TipoServico.query.get_or_404(id)
    tipo.nome = ''
    db.session.commit()
    return redirect(url_for('cadastro_tipo_servico', id=tipo.id))

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

@app.route('/ordem_servico/<int:os_id>/imprimir')
def imprimir_os(os_id):
    os = OrdemServico.query.get_or_404(os_id)
    return render_template('impressao_os.html', os=os)

@app.route('/ordem_servico/<int:os_id>/pdf')
def pdf_os(os_id):
    os = OrdemServico.query.get_or_404(os_id)
    rendered = render_template('impressao_os.html', os=os)
    pdf = gerar_pdf(rendered)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=os_{os_id}.pdf'
    return response

def gerar_pdf(html_content):
    """
    Gera um PDF simples a partir de HTML usando FPDF.
    Este exemplo converte o HTML em texto simples.
    Para HTML completo, use uma biblioteca como xhtml2pdf ou WeasyPrint.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Remove tags HTML para texto simples
    import re
    text = re.sub('<[^<]+?>', '', html_content)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S').encode('latin1')

# Relatório do Cliente (resumo simples)
@app.route('/ordem_servico/<int:os_id>/relatorio_cliente')
def relatorio_cliente(os_id):
    os = OrdemServico.query.get_or_404(os_id)
    # Parse dos serviços e produtos
    try:
        servicos = json.loads(os.servicos) if os.servicos else []
    except Exception:
        servicos = []
    try:
        produtos = json.loads(os.produtos) if os.produtos else []
    except Exception:
        produtos = []
    return render_template(
        'relatorio_cliente.html',
        os=os,
        servicos=servicos,
        produtos=produtos
    )

# Relatório Técnico Completo (igual cadastro_ordem_servico)
@app.route('/ordem_servico/<int:os_id>/relatorio_os')
def relatorio_os(os_id):
    os = OrdemServico.query.get_or_404(os_id)
    clientes = Cliente.query.all()
    tipos_servico = TipoServico.query.all()
    servicos_os = []
    produtos_os = []
    if os and os.servicos:
        try:
            servicos_os = json.loads(os.servicos)
        except Exception:
            servicos_os = []
    if os and os.produtos:
        try:
            produtos_os = json.loads(os.produtos)
        except Exception:
            produtos_os = []
    servicos = Servico.query.all()
    produtos = Produto.query.all()
    return render_template(
        'cadastro_ordem_servico.html',
        os=os,
        clientes=clientes,
        tipos_servico=tipos_servico,
        produtos_os=produtos_os,
        servicos_os=servicos_os,  # <-- Adicione isso!
        servicos=servicos,
        produtos=produtos,
        relatorio=True  # Use esta flag no template para modo somente leitura, se desejar
    )

def ordem_servico_to_dict(os):
    if not os:
        return None
    cliente = os.cliente if hasattr(os, "cliente") and os.cliente else None
    return {
        "id": os.id,
        "codigo": os.codigo,
        "data_emissao": os.data_emissao.strftime('%Y-%m-%d') if os.data_emissao else '',
        "previsao_conclusao": os.previsao_conclusao.strftime('%Y-%m-%d') if os.previsao_conclusao else '',
        "tipo_servico": os.tipo_servico,
        "tecnico": os.tecnico,
        "hora_inicio": os.hora_inicio,
        "hora_termino": os.hora_termino,
        "total_horas": os.total_horas,
        "km_inicial": os.km_inicial,
        "km_final": os.km_final,
        "km_total": os.km_total,
        "servicos_json": os.servicos_json if hasattr(os, "servicos_json") else [],
        "produtos_json": os.produtos_json if hasattr(os, "produtos_json") else [],
        "cliente": {
            "id": cliente.id if cliente else '',
            "cpf_cnpj": cliente.cpf_cnpj if cliente else '',
            "telefone": cliente.telefone if cliente else '',
            "email": cliente.email if cliente else '',
            "endereco": cliente.endereco if cliente else '',
            "nome": cliente.nome if cliente else ''
        } if cliente else None,
        # Adicione outros campos que precisar
    }

# EXECUTAR
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


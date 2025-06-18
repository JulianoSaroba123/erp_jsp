from flask import Flask, render_template, request, redirect, send_file
from models.cliente_model import db, Cliente
import pandas as pd
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

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
fr

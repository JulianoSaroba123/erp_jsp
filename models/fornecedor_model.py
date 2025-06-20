from models import db

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    cep = db.Column(db.String(9), nullable=True)
    endereco = db.Column(db.String(150), nullable=True)
    cidade = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"

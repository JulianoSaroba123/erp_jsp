from models import db

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False, unique=True)  # <-- Adicione essa linha
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"

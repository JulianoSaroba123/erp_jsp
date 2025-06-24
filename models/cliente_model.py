from models import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf_cnpj = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(150), nullable=True)
    numero = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"<Cliente {self.nome}>"

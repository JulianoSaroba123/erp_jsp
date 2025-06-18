from models import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20))
    nome = db.Column(db.String(100))
    cpf_cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    numero = db.Column(db.String(10))

    def __repr__(self):
        return f'<Cliente {self.nome}>'

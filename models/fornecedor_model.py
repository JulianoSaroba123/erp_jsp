from models import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    cep = db.Column(db.String(20))
    cidade = db.Column(db.String(100))
    endereco = db.Column(db.String(200))

    def __repr__(self):
        return f"<Fornecedor {self.codigo} - {self.nome}>"
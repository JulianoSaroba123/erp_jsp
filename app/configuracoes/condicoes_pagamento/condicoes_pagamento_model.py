from app.extensoes import db

class CondicaoPagamento(db.Model):
	__tablename__ = 'condicoes_pagamento'

	id = db.Column(db.Integer, primary_key=True)
	descricao = db.Column(db.String(100))
	tipo = db.Column(db.String(20))
	parcelas = db.Column(db.Integer, default=1)
	desconto = db.Column(db.Float, default=0.0)
	juros = db.Column(db.Float, default=0.0)
	observacoes = db.Column(db.Text)

	def __repr__(self):
		return f"<Condição {self.descricao}>"

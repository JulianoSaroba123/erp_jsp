# models/tag_model.py

from models import db

class Tag(db.Model):
    _tablename_ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), unique=True, nullable=False)       # Ex: {{cliente_nome}}
    descricao = db.Column(db.String(255), nullable=True)               # Ex: "Nome do cliente"
    modulo = db.Column(db.String(50), nullable=True)                   # Ex: "Cliente", "OS", etc.

    def _repr_(self):
        return f"<Tag {self.tag}>"

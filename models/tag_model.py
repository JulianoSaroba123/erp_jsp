# models/tag_model.py
from models.db_config import db

class Tag(db.Model):
    __tablename__ = 'tags'  # ✅ Corrigido

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), unique=True, nullable=False)       # Ex: {{cliente_nome}}
    descricao = db.Column(db.String(255), nullable=True)               # Ex: "Nome do cliente"
    modulo = db.Column(db.String(50), nullable=True)                   # Ex: "Cliente", "OS", etc.

    def __repr__(self):  # ✅ Corrigido
        return f"<Tag {self.tag}>"

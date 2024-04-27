from werkzeug.security import generate_password_hash, check_password_hash
from api.databases.config import db
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "documento": self.documento,
            "username": self.username,
            "email": self.email,
            "ativo": self.ativo
        }

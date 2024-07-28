from typing import Any
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
    deleted_at = db.Column(db.DateTime)

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
        
class Group(db.Model):
    __tablename__ = 'groups'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "ativo": self.ativo,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Permission(db.Model):
    __tablename__ = 'permissions'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)

class UserPermission(db.Model):
    __tablename__ = 'users_permissions'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('auth.permissions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('auth.users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)

    permission = db.relationship('Permission', backref='user_permissions')
    user = db.relationship('User', backref='user_permissions')

class GroupPermission(db.Model):
    __tablename__ = 'group_permissions'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('auth.permissions.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('auth.groups.id'))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)

    permission = db.relationship('Permission', backref='group_permissions')
    group = db.relationship('Group', backref='group_permissions')

class GroupUser(db.Model):
    __tablename__ = 'users_group'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth.users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('auth.groups.id'))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)

    user = db.relationship('User', backref='groups')
    group = db.relationship('Group', backref='users')

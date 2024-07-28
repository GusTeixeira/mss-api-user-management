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
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=True)

    permission = db.relationship('Permission')
    user = db.relationship('User')

class GroupPermission(db.Model):
    __tablename__ = 'group_permissions'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)

    permission = db.relationship('Permission')
    group = db.relationship('Group')

class GroupUser(db.Model):
    __tablename__ = 'users_group'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), nullable=True)

    user = db.relationship('User')
    group = db.relationship('Group')

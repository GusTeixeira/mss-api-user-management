import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from api.models.user_models import User
from api.databases.config import db

class UserRepository:

    def find_by_username(self, username):
        try:
            return db.session.scalars(select(User).where(User.username == username)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao buscar usuário pelo username: {e}")
    
    def find_by_username(self, username):
        try:
            return db.session.scalars(select(User).where(User.username == username)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao buscar usuário pelo username: {e}")

    def find_by_id(self, id):
        try:
            return db.session.scalars(select(User).where(User.id == id)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro buscando usuario pelo id: {e}")

    def create_user(self, nome, documento, username, password, email):
        try:
            new_user = User(
                nome=nome,
                documento=documento,
                username=username,
                email=email,
                ativo=True
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            new_user_dict = new_user.to_dict()
            return new_user_dict
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao criar usuário: {e}")

    def delete_user_by_id(self, id):
        try:
            user = db.session.scalars(select(User).where(User.id == id)).first()
            if user:
                user.deleted_at = datetime.datetime.now(tz=None)
                user.ativo = False
                db.session.commit()
                return True
            else:
                raise ValueError("usuario não encontrado")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao deletar usuario: {e}")

    def find_password_by_username(self, username):
        try:
            return db.session.scalars(select(User.password).where(User.username == username)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao buscar usuario: {e}")

    def compare_passwords(self, password, input_password):
        try:
            return User.check_password(password, input_password)
        except Exception as e:
            raise e

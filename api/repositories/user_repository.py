from curses.ascii import US
import datetime
from typing import Any, Literal
from click import Group
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from api.models.user_models import User
from api.databases.config import db

class UserRepository:

    def find_users(self, documento=None, username=None, email=None, ativo=None):
        try:
            query = select(User)
            conditions = []

            if documento:
                conditions.append(User.documento.ilike(f'%{documento}%'))
            if username:
                conditions.append(User.username.ilike(f'%{username}%'))
            if email:
                conditions.append(User.email.ilike(f'%{email}%'))
            if ativo is not None:
                conditions.append(User.ativo == ativo)

            if conditions:
                query = query.where(*conditions)

            return db.session.scalars(query).all()

        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao buscar usuários: {e}")
        
    def find_by_username(self, username) -> User | None:
        try:
            return db.session.scalars(select(User).where(User.username == username)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro ao buscar usuário pelo username: {e}")
    
    def find_by_id(self, id) -> User | None:
        try:
            return db.session.scalars(select(User).where(User.id == id)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro buscando usuario pelo id: {e}")

    def create_user(self, nome, documento, username, password, email) -> dict[str, Any]:
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
            
            new_user = new_user.to_dict()
            
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro ao criar usuário: {e}")

    def delete_user_by_id(self, id) -> Literal[True]:
        try:
            user = db.session.scalars(select(User).where(User.id == id)).first()
            if user:
                user.deleted_at = datetime.datetime.now(tz=None)
                user.ativo = False
                db.session.commit()
                return True
            else:
                raise SQLAlchemyError("usuario não encontrado")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro ao deletar usuario: {e}")
    
    def update_user(self, id, nome=None, documento=None, username=None, email=None) -> dict[str, Any]:
        try:
            user = db.session.scalars(select(User).where(User.id == id)).first()
            if user:
                user.updated_at = datetime.datetime.now(tz=None)
                if nome:
                    user.nome = nome
                if documento:
                    user.documento = documento
                if username:
                    user.username = username
                if email:
                    user.email = email
            else:
                db.session.rollback()
                raise SQLAlchemyError("usuario não encontrado")
            db.session.commit()
            
            return user.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro ao atualizar usuario: {e}")

    def find_password_by_username(self, username) -> Any | None:
        try:
            return db.session.scalars(select(User.password).where(User.username == username)).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro ao buscar usuario: {e}")

    def compare_passwords(self, password, input_password) -> bool:
        try:
            return User.check_password(password, input_password)
        except Exception as e:
            raise e

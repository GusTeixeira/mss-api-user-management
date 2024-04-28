from sqlalchemy import select
from api.models.user_models import User
from api.databases.config import db
class UserRepository:

    def find_by_username(self, username):
        return db.session.scalars(select(User.username).where(User.username==username)).first()

    def create_user(self, nome, documento, username, password, email):
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



from sqlalchemy import desc, select
from api.models.user_models import Group
from api.databases.config import db
from sqlalchemy.exc import SQLAlchemyError

class GroupRepository:
    
    def create_group(self, nome, descricao):
        try:
            new_group = Group(
                nome=nome,
                descricao=descricao,
                ativo=True,
            )
            db.session.add(new_group)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"erro ao criar novo grupo: {e}")
    
    def find_groups(self, nome=None,id=None):
        try:
            query = select(Group)
            if nome:
                query = query.filter(Group.nome == nome)
            if id:
                query = query.filter(Group.id == id)
        
            return db.session.scalars(query).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"erro ao buscar grupos: {e}")
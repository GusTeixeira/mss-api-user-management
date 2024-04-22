from flask import jsonify
from api.models.user_models import User

def create_user(nome, documento, username, password, email):

    exists = User.query.filter_by(username=username).first()
    
    if exists:
        return jsonify({'error': 'Nome de usuário já está em uso'}), 409
    
    
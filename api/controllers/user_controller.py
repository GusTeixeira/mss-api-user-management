from flask import jsonify
from api.repositories.user_repository import UserRepository

def create_user(nome, documento, username, password, email):
    user_repo = UserRepository()
    find_user = user_repo.find_by_username(username)
    
    if find_user:
        return jsonify({'error': 'Nome de usuário já está em uso'}), 409
    
    created_user = user_repo.create_user(nome, documento, username, password, email)
    
    return jsonify({'dados':created_user}), 200
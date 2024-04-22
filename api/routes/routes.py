from flask import Blueprint, request

auth = Blueprint('auth', __name__)

"""ROTA PARA REGISTRO DE NOVO USUÁRIO"""
@auth.route('/register', methods=['POST'])
def register():
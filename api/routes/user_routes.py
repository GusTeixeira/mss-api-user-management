import json
from typing import Literal
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from api.schemas.user_schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from api.controllers.user_controller import create_user, authenticate_user, delete_user

auth = Blueprint('auth', __name__,url_prefix='/auth')

@auth.route("/health", methods=['GET'])
def hello_world() -> tuple[Response, Literal[200]]:
    return jsonify({"msg":"Olá, a api de autenticação do MSS está funcionando corretamente"}),200

@auth.route("/register", methods=['POST'])
def register() -> tuple[Response, Literal[400]] | tuple[Response, Literal[200]]:
    user_schema = UserSchema()

    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"erro": "payload inválido"}), 400

    try:
        created_user = create_user(user_data['nome'], user_data['documento'], user_data['username'], user_data['password'], user_data['email'])
    except ValueError as err:
        return jsonify({"msg": str(err)}), 400
    
    return jsonify({"msg": "successful", "dados": created_user}), 200

@auth.route("/delete/<int:id>", methods=['DELETE'])
def delete(id) -> tuple[Response, Literal[500]] | tuple[Response, Literal[200]]:
    try:
        success = delete_user(id)
        if not success:
            return jsonify({"msg": "erro ao deletar usuário"}), 500
    except ValueError as err:
        return jsonify({"msg": "erro ao deletar usuário: "+str(err)}), 500
    
    return jsonify({"msg": "successful"}), 200

@auth.route("/token", methods=['POST'])
def login() -> tuple[Response, Literal[400]] | tuple[Response, Literal[200]]:
    login_schema = LoginSchema()
    
    try:
        user_data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"erro": "payload inválido"}), 400
    
    try:
        login = authenticate_user(user_data['username'], user_data['password'])
    except ValueError as err:
        return jsonify({"msg": "erro ao autenticar usuário: "+str(err)}), 400
    
    return jsonify({"msg": "successful"}), 200

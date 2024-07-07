import json
from flask import Blueprint, jsonify, request
from api.schemas.user_schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from api.controllers.user_controller import create_user, authenticate_user, delete_user

auth = Blueprint('auth', __name__)

@auth.route("/hello", methods=['GET'])
def hello_world():
    return jsonify({"dados":"Hello, World!"}),200

@auth.route("/auth/register", methods=['POST'])
def register():
    user_schema = UserSchema()

    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"erro": "payload inválido"}), 400
    
    try:
        created_user = create_user(user_data['nome'], user_data['documento'], user_data['username'], user_data['password'], user_data['email'])
    except ValueError as err:
        return jsonify({"msg": "erro ao criar usuário: "+str(err)}), 400
    
    return jsonify({"msg": "successful", "dados": created_user}), 200

@auth.route("/auth/delete/<int:id>", methods=['DELETE'])
def delete(id):
    try:
        success = delete_user(id)
    except ValueError as err:
        return jsonify({"msg": "erro ao deletar usuário: "+str(err)}), 400
    
    return jsonify({"msg": "user delete: "+success}), 200

@auth.route("/auth/token", methods=['POST'])
def login():
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

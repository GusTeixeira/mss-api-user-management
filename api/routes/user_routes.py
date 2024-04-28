import json
from flask import Blueprint, jsonify, request
from api.schemas.user_schemas import UserSchema
from marshmallow import ValidationError
from api.controllers.user_controller import create_user

auth = Blueprint('auth', __name__)

@auth.route("/hello", methods=['GET'])
def hello_world():
    return jsonify({"dados":"Hello, World!"}),200

@auth.route("/register", methods=['POST'])
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

    
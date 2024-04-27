import json
from flask import Blueprint, jsonify, request
from api.schemas.user_schemas import UserSchema
from marshmallow import ValidationError
from api.controllers.user_controller import create_user

auth = Blueprint('auth', __name__)

@auth.route("/", methods=['GET'])
def hello_world():
    return jsonify({"dados":"Hello, World!"}),200

@auth.route("/register", methods=['POST'])
def register():
    schema = UserSchema()
    
    try:
        result = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"erro":"payload inválido"}),400
    
    response = create_user(result['nome'], result['documento'], result['username'], result['password'], result['email'])

    return response
    
    
    
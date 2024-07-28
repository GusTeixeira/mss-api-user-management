import json
from typing import Literal
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from sqlalchemy import Update
from api.repositories.user_repository import UserRepository
from api.schemas.user_schemas import UpdateUserSchema, UserSchema
from marshmallow import ValidationError
from pycpfcnpj import cpf, cnpj
from sqlalchemy.exc import SQLAlchemyError


auth = Blueprint('auth', __name__,url_prefix='/user')
user_repo = UserRepository()

@auth.route("/health", methods=['GET'])
def hello_world() -> tuple[Response, Literal[200]]:
    return jsonify({"msg":"Olá, a api de autenticação do MSS está funcionando corretamente"}),200

@auth.route("/", methods=['POST'])
def register() -> tuple[Response, Literal[400]] | tuple[Response, Literal[200]]:
    user_schema = UserSchema()

    try:
        user_data = user_schema.load(request.json)
        
        user_data["nome"] = user_data["nome"].upper()
        
        validacao_cpf = cpf.validate(user_data["documento"])
        validacao_cnpj = cnpj.validate(user_data["documento"])

        if not validacao_cpf and not validacao_cnpj:
            return jsonify({"error":"documento inválido"}), 400
       
        find_user = user_repo.find_by_username(user_data["username"])
        
        if find_user and find_user.ativo == True:
            return jsonify({"error":"usuario ativo com mesmo username já existente"}), 400
        
        created_user = user_repo.create_user(user_data["nome"], user_data["documento"], user_data["username"], user_data["password"], user_data["email"])
        
        return jsonify({"msg": "successful", "dados": created_user}), 200
    
    except ValidationError as err:
        return jsonify({"error": "payload inválido"}), 400
    except SQLAlchemyError as err:
        return jsonify({"msg": str(err)}), 400

@auth.route("/",methods=['GET'])
def get() -> tuple[Response, Literal[200]] | tuple[Response, Literal[500]]:
    documento = request.args.get("documento") 
    username = request.args.get("username")
    email = request.args.get("email")
    ativo = request.args.get("ativo")
    
    try:
        if ativo:
            if ativo.upper() == "FALSE":
                ativo = False
            elif ativo.upper() == "TRUE":
                ativo = True
            else:
                return jsonify({"error":"parametro de ativo invalido"}), 400
    
        if documento:
            validacao_cpf = cpf.validate(documento)
            validacao_cnpj = cnpj.validate(documento)
            
            if not validacao_cpf and not validacao_cnpj:
                 return jsonify({"error":"documento inválido"}), 400
            
        users = user_repo.find_users(documento, username, email, ativo)
        users_list = []
        if users:
            users_list = [user.to_dict() for user in users]
        
        return jsonify({"msg":"successful", "dados": users_list}), 200
    except SQLAlchemyError as err:
        return jsonify({"error":"erro ao listar usuarios: "+str(err)}), 500

@auth.route("/<int:id>",methods=['GET'])
def get_by_id(id) -> tuple[Response, Literal[200]] | tuple[Response, Literal[500]]:
    try:
        user = user_repo.find_by_id(id)
        if user:
            user = user.to_dict()
        else:
            user = []
        return jsonify({"msg":"successful", "dados": user}), 200
    except SQLAlchemyError as e:
        return jsonify({"error":e}), 500

@auth.route("/<int:id>",methods=['PUT'])
def update_by_id(id) -> Response | tuple[Response, Literal[400]] | tuple[Response, Literal[500]]:
    update_user_schema = UpdateUserSchema()

    try:
        update_fields = update_user_schema.load(request.json)
        
        if update_fields.get("username"):
            find_user = user_repo.find_by_username(update_fields.get("username"))
            if find_user and find_user.ativo == True:
                return jsonify({"error":"usuario ativo com mesmo username já existente"})
            
        updated_user = user_repo.update_user(id, update_fields.get("nome"), update_fields.get("documento"), update_fields.get("username"), update_fields.get("email"))
        return jsonify({"msg":"successful", "dados":updated_user})
    except ValidationError as e:
        return jsonify({"error": f"payload inválido: {e}"}), 400
    except SQLAlchemyError as e:
        return jsonify({"error":e}), 500
    
@auth.route("/<int:id>", methods=['DELETE'])
def delete(id) -> tuple[Response, Literal[500]] | tuple[Response, Literal[200]]:
    try:
        success = user_repo.delete_user_by_id(id)
        if not success:
            return jsonify({"error": "erro ao deletar usuário"}), 500
        return jsonify({"msg": "successful"}), 200
    except SQLAlchemyError as err:
        return jsonify({"msg": "erro ao deletar usuário: "+str(err)}), 500

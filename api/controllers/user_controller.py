from pycpfcnpj import cpf, cnpj
from email_validator import validate_email, EmailNotValidError
from api.repositories.user_repository import UserRepository
from api.models.user_models import User

user_repo = UserRepository()
def create_user(nome, documento, username, password, email):    
    nome = nome.upper()
    validacao_cpf = cpf.validate(documento)
    validacao_cnpj = cnpj.validate(documento)
    
    if not validacao_cpf and not validacao_cnpj:
        raise ValueError("documento inválido")
    
    try:
        find_user = user_repo.find_by_username(username)
    except Exception as error:
        raise error
    
    if find_user and find_user.ativo == True:
        raise ValueError("usuário ativo com o mesmo username já existente")
    
    try:
        validate_email(email)
    except EmailNotValidError:
        raise ValueError("email inválido ou inexistente")
    
    try:
        created_user = user_repo.create_user(nome, documento, username, password, email)
    except Exception as error:
        raise error
    
    return created_user

def delete_user(id):
    try:
        success = user_repo.delete_user_by_id(id)
        if not success:
            raise ValueError("erro ao deletar usuario")
    except Exception as e:
        raise e
    
    return success
    
def authenticate_user(username, password):
    
    find_user = user_repo.find_by_username(username)
    
    if not find_user:
        raise ValueError("verifique seu usuário ou senha")
    
    hash_password = user_repo.find_password_by_username(username)
    
    if not hash_password:
        raise ValueError("verifique seu usuário ou senha")
    
    valid_login = user_repo.compare_passwords(hash_password, password)
    
    if valid_login:
        return True
    
from pycpfcnpj import cpf, cnpj
from email_validator import validate_email, EmailNotValidError
from api.repositories.user_repository import UserRepository

def create_user(nome, documento, username, password, email):
    user_repo = UserRepository()
    
    nome = nome.upper()
    
    validacao_cpf = cpf.validate(documento)
    validacao_cnpj = cnpj.validate(documento)
    
    if not validacao_cpf and not validacao_cnpj:
        raise ValueError("documento inválido")
    
    find_user = user_repo.find_by_username(username)
    
    if find_user:
        raise ValueError("usuário com o mesmo username já existente")
    
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise ValueError("email inválido ou inexistente")
    
    created_user = user_repo.create_user(nome, documento, username, password, email)
    
    return created_user

def authenticate_user(username, password):
    user_repo = UserRepository()
    
    find_user = user_repo.find_by_username(username)
    
    if not find_user:
        raise ValueError("verifique seu usuário ou senha")
    
    hash_password = user_repo.find_password_by_username(username)
    
    if not hash_password:
        raise ValueError("verifique seu usuário ou senha")
    
    valid_login = user_repo.compare_passwords(hash_password, password)
    
    if valid_login:
        return True
    
from database import *
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta_muito_segura"  # Substitua por uma chave segura
ALGORITHM = "HS256"  # Algoritmo de hash
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiração do token em minutos

def verificar_login(login: str, senha: str) -> bool:
    try:
        # Tenta encontrar um registro com o login fornecido
        empresa = Empresa.get(Empresa.login == login)
        
        # Verifica se a senha coincide
        if empresa.senha == senha:
            return True
        else:
            return False
    except Empresa.DoesNotExist:
        # Caso o login não seja encontrado
        return False
    
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna as informações contidas no token
    except JWTError:
        return None  # Token inválido ou expirado
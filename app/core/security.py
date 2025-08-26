from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import user_model
from app.database import get_db  

SECRET_KEY = "sua_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar se a senha está correta
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para criar o token de acesso
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para decodificar o token de acesso
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Retorna o ID do usuário
    except JWTError:
        return None

# Função para obter o usuário atual a partir do token
def get_current_user_from_token(token: str, db: Session) -> user_model.User:
    try:
        # Decodificar o token e obter o ID do usuário
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # O 'sub' contém o ID do usuário

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
        
        # Garantir que o user_id seja um número inteiro, caso seja necessári
        
        # Buscar o usuário no banco de dados
        user = db.query(user_model.User).filter(user_model.User.username == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")


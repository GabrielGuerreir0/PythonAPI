from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from .. import schemas
import base64
from ..database import get_db
from app.core.security import get_password_hash, get_current_user_from_token  # Corrigido para usar a função

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    full_name: str = Form(None, max_length=50),
    password: str = Form(..., min_length=6),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Verificar se o usuário já existe
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso.")
    
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email já está registrado.")

    # Criptografar a senha
    hashed_password = get_password_hash(password)

    # Ler o arquivo da imagem em binário, se fornecido
    profile_image_data = await profile_image.read() if profile_image else None

    # Criar novo usuário
    new_user = models.User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        profile_image=profile_image_data
    )

    # Salvar no banco de dados
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso!", "user_id": new_user.id}

# READ - Obter Usuário por ID
@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Codificar a imagem para Base64, se existir
    profile_image_base64 = (
        base64.b64encode(user.profile_image).decode('utf-8') 
        if user.profile_image 
        else None
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "profile_image": profile_image_base64
    }

# READ - Listar Todos os Usuários
@router.get("/users", response_model=List[schemas.UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# UPDATE - Atualizar Usuário
@router.put("/users/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: int,
    username: Optional[str] = Form(None, min_length=3, max_length=20),
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None, max_length=50),
    password: Optional[str] = Form(None, min_length=6),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if username:
        user.username = username
    if email:
        user.email = email
    if full_name:
        user.full_name = full_name
    if password:
        user.hashed_password = get_password_hash(password)
    if profile_image:
        user.profile_image = await profile_image.read()

    db.commit()
    db.refresh(user)

    # Codificar a imagem para Base64, se existir
    profile_image_base64 = (
        base64.b64encode(user.profile_image).decode('utf-8') 
        if user.profile_image 
        else None
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "profile_image": profile_image_base64
    }

# DELETE - Deletar Usuário
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(user)
    db.commit()

    return {"message": "Usuário deletado com sucesso."}

@router.get("/me/{token}", response_model=schemas.UserOut)
def read_current_user(token: str = Path(..., description="Token de autenticação"), db: Session = Depends(get_db)):
    # Usar a função para obter o usuário a partir do token
    current_user = get_current_user_from_token(token, db)  # Ajuste essa função para lidar com o token

    # Codificar a imagem para Base64, se existir
    profile_image_base64 = (
        base64.b64encode(current_user.profile_image).decode('utf-8') 
        if current_user.profile_image 
        else None
    )

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "profile_image": profile_image_base64
    }

# READ - Obter Usuário por Nome de Usuário
@router.get("/users/username/{username}", response_model=schemas.UserOut)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    # Verificar se o usuário existe
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Codificar a imagem para Base64, se existir
    profile_image_base64 = (
        base64.b64encode(user.profile_image).decode('utf-8') 
        if user.profile_image 
        else None
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "profile_image": profile_image_base64
    }

@router.put("/users/{user_id}/password", response_model=schemas.UserOut)
async def update_user_password(
    user_id: int,
    password: str = Form(..., min_length=6),
    db: Session = Depends(get_db)
):
    # Verifica se o usuário existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Atualiza a senha do usuário
    user.hashed_password = get_password_hash(password)

    # Commit e refresh para salvar a alteração no banco
    db.commit()
    db.refresh(user)

    # Codificar a imagem para Base64, se existir
    profile_image_base64 = (
        base64.b64encode(user.profile_image).decode('utf-8') 
        if user.profile_image 
        else None
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "profile_image": profile_image_base64
    }

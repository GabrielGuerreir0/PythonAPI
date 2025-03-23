# app/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import user_model
from app.schemas import user_schema
from app.core.security import get_password_hash, get_current_user_from_token
from typing import Optional
import base64


def register_user_service(username, email, full_name, password, profile_image_data, db: Session):
    # Verificar se usuário já existe
    if db.query(user_model.User).filter(user_model.User.username == username).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso.")
    
    if db.query(user_model.User).filter(user_model.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email já está registrado.")

    hashed_password = get_password_hash(password)

    new_user = user_model.User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        profile_image=profile_image_data
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso!", "user_id": new_user.id}


def get_user_by_id_service(user_id: int, db: Session):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    return serialize_user(user)


def get_users_service(skip: int, limit: int, db: Session):
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return [serialize_user(user) for user in users]


def update_user_service(user_id: int, username: Optional[str], email: Optional[str], full_name: Optional[str], password: Optional[str], profile_image_data, db: Session):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
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
    if profile_image_data:
        user.profile_image = profile_image_data

    db.commit()
    db.refresh(user)

    return serialize_user(user)


def delete_user_service(user_id: int, db: Session):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado com sucesso."}


def get_current_user_service(token: str, db: Session):
    current_user = get_current_user_from_token(token, db)
    return serialize_user(current_user)


def get_user_by_username_service(username: str, db: Session):
    user = db.query(user_model.User).filter(user_model.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    return serialize_user(user)


def update_user_password_service(user_id: int, password: str, db: Session):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    user.hashed_password = get_password_hash(password)
    db.commit()
    db.refresh(user)

    return serialize_user(user)


def serialize_user(user):
    profile_image_base64 = (
        base64.b64encode(user.profile_image).decode('utf-8')
        if user.profile_image else None
    )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "profile_image": profile_image_base64
    }

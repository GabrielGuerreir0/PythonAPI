from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import user_schema
from ..database import get_db
from ..services import user_service

router = APIRouter()

# REGISTER
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    full_name: str = Form(None, max_length=50),
    password: str = Form(..., min_length=6),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    profile_image_data = await profile_image.read() if profile_image else None
    return user_service.register_user_service(username, email, full_name, password, profile_image_data, db)

# READ - Obter Usuário por ID
@router.get("/users/{user_id}", response_model=user_schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id_service(user_id, db)

# READ - Listar Usuários
@router.get("/users", response_model=List[user_schema.UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_service.get_users_service(skip, limit, db)

# UPDATE - Atualizar Usuário
@router.put("/users/{user_id}", response_model=user_schema.UserOut)
async def update_user(
    user_id: int,
    username: Optional[str] = Form(None, min_length=3, max_length=20),
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None, max_length=50),
    password: Optional[str] = Form(None, min_length=6),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    profile_image_data = await profile_image.read() if profile_image else None
    return user_service.update_user_service(user_id, username, email, full_name, password, profile_image_data, db)

# DELETE
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user_service(user_id, db)

# READ - Obter Usuário Atual pelo Token
@router.get("/me/{token}", response_model=user_schema.UserOut)
def read_current_user(token: str = Path(...), db: Session = Depends(get_db)):
    return user_service.get_current_user_service(token, db)

# READ - Obter Usuário por Username
@router.get("/users/username/{username}", response_model=user_schema.UserOut)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return user_service.get_user_by_username_service(username, db)

# UPDATE - Atualizar Senha
@router.put("/users/{user_id}/password", response_model=user_schema.UserOut)
async def update_user_password(
    user_id: int,
    password: str = Form(..., min_length=6),
    db: Session = Depends(get_db)
):
    return user_service.update_user_password_service(user_id, password, db)

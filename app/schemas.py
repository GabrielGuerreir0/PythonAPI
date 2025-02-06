from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import time, date, datetime
from fastapi import UploadFile, File

# -------- Paciente --------
class PacienteCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    idade: int = Field(..., gt=0, lt=150)
    historico_medico: Optional[str] = Field(None, max_length=500)

    class Config:
        from_orm = True


class PacienteOut(PacienteCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_orm = True


class PacienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=50)
    idade: Optional[int] = Field(None, gt=0, lt=150)
    historico_medico: Optional[str] = Field(None, max_length=500)

    class Config:
        from_orm = True


# -------- Médico --------
class MedicoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    especialidade: str = Field(..., min_length=3, max_length=100)

    class Config:
        from_orm = True


class MedicoCreate(MedicoBase):
    pass


class MedicoOut(MedicoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_orm = True


# -------- Consulta --------
class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data: date
    hora: time
    descricao: Optional[str] = Field(None, max_length=500)

    class Config:
        from_orm = True


class ConsultaOut(ConsultaCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_orm = True


# -------- Usuário --------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=50)
    password: str = Field(..., min_length=6)
    profile_image: Optional[UploadFile] = None

    class Config:
        from_orm = True

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    profile_image: Optional[str] = None  # Agora suporta Base64


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str


# -------- Autenticação --------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# -------- Resposta de Erro --------
class ErrorResponse(BaseModel):
    detail: str

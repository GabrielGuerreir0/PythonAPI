from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PacienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    idade: int = Field(..., gt=0, lt=150)
    historico_medico: Optional[str] = Field(None, max_length=500)

    class Config:
        orm_mode = True

class PacienteCreate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PacienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=50)
    idade: Optional[int] = Field(None, gt=0, lt=150)
    historico_medico: Optional[str] = Field(None, max_length=500)

    class Config:
        orm_mode = True

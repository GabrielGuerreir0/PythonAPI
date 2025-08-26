from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MedicoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    especialidade: str = Field(..., min_length=3, max_length=100)

    class Config:
        orm_mode = True

class MedicoCreate(MedicoBase):
    pass

class MedicoOut(MedicoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

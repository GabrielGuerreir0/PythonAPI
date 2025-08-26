from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime

class ConsultaBase(BaseModel):
    paciente_id: int
    medico_id: int
    data: date
    hora: time
    descricao: Optional[str] = Field(None, max_length=500)

    class Config:
        orm_mode = True

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaOut(ConsultaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

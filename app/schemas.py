from pydantic import BaseModel
from typing import Optional
from datetime import time, date

# Modelo para criação de um paciente
class PacienteCreate(BaseModel):
    nome: str
    idade: int
    historico_medico: str

    class Config:
        from_attributes = True  

# Modelo para o retorno de informações sobre o paciente
class PacienteOut(PacienteCreate):
    id: int

    class Config:
        from_attributes = True

# Modelo para atualização de um paciente
class PacienteUpdate(BaseModel):
    nome: Optional[str]
    idade: Optional[int]
    historico_medico: Optional[str]

    class Config:
        from_attributes = True

# Modelo para um médico
class MedicoBase(BaseModel):
    nome: str
    especialidade: str

    class Config:
        from_attributes = True

class MedicoCreate(MedicoBase):
    pass  

class MedicoOut(MedicoBase):
    id: int

    class Config:
        from_attributes = True

# Modelo para consulta
class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data: date
    hora: time
    descricao: str

    class Config:
        from_attributes = True

class ConsultaOut(ConsultaCreate):
    id: int

    class Config:
        from_attributes = True

# Modelo para retorno de erro, caso necessário
class ErrorResponse(BaseModel):
    detail: str

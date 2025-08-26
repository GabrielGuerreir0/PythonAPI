from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import paciente_schema
from app.services.paciente_service import (
    create_paciente_service,
    get_all_pacientes_service,
    get_paciente_by_id_service,
    update_paciente_service,
    delete_paciente_service
)

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um paciente
@router.post("/", response_model=paciente_schema.PacienteOut)
def create_paciente(paciente: paciente_schema.PacienteCreate, db: Session = Depends(get_db)):
    return create_paciente_service(db, paciente)

# Rota para listar todos os pacientes
@router.get("/", response_model=list[paciente_schema.PacienteOut])
def get_pacientes(db: Session = Depends(get_db)):
    return get_all_pacientes_service(db)

# Rota para obter um paciente por ID
@router.get("/{paciente_id}", response_model=paciente_schema.PacienteOut)
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return get_paciente_by_id_service(db, paciente_id)

# Rota para atualizar um paciente
@router.put("/{paciente_id}", response_model=paciente_schema.PacienteOut)
def update_paciente(paciente_id: int, paciente: paciente_schema.PacienteCreate, db: Session = Depends(get_db)):
    return update_paciente_service(db, paciente_id, paciente)

# Rota para deletar um paciente
@router.delete("/{paciente_id}", response_model=paciente_schema.PacienteOut)
def delete_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return delete_paciente_service(db, paciente_id)

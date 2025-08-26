from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import medico_schema
from app.services.medico_service import (
    create_medico_service,
    get_all_medicos_service,
    get_medico_by_id_service,
    update_medico_service,
    delete_medico_service
)

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um médico
@router.post("/", response_model=medico_schema.MedicoOut)
def create_medico(medico: medico_schema.MedicoCreate, db: Session = Depends(get_db)):
    return create_medico_service(db, medico)

# Rota para listar todos os médicos
@router.get("/", response_model=list[medico_schema.MedicoOut])
def get_medicos(db: Session = Depends(get_db)):
    return get_all_medicos_service(db)

# Rota para obter um médico por ID
@router.get("/{medico_id}", response_model=medico_schema.MedicoOut)
def get_medico(medico_id: int, db: Session = Depends(get_db)):
    return get_medico_by_id_service(db, medico_id)

# Rota para atualizar um médico
@router.put("/{medico_id}", response_model=medico_schema.MedicoOut)
def update_medico(medico_id: int, medico: medico_schema.MedicoCreate, db: Session = Depends(get_db)):
    return update_medico_service(db, medico_id, medico)

# Rota para deletar um médico
@router.delete("/{medico_id}", response_model=medico_schema.MedicoOut)
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    return delete_medico_service(db, medico_id)

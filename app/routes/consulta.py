from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import consulta_schema
from app.services.consulta_service import (
    create_consulta_service,
    get_all_consultas_service,
    get_consulta_by_id_service,
    update_consulta_service,
    delete_consulta_service
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=consulta_schema.ConsultaOut)
def create_consulta(consulta: consulta_schema.ConsultaCreate, db: Session = Depends(get_db)):
    return create_consulta_service(db, consulta)


@router.get("/", response_model=list[consulta_schema.ConsultaOut])
def get_consultas(db: Session = Depends(get_db)):
    return get_all_consultas_service(db)


@router.get("/{consulta_id}", response_model=consulta_schema.ConsultaOut)
def get_consulta(consulta_id: int, db: Session = Depends(get_db)):
    return get_consulta_by_id_service(db, consulta_id)


@router.put("/{consulta_id}", response_model=consulta_schema.ConsultaOut)
def update_consulta(consulta_id: int, consulta: consulta_schema.ConsultaCreate, db: Session = Depends(get_db)):
    return update_consulta_service(db, consulta_id, consulta)


@router.delete("/{consulta_id}", response_model=consulta_schema.ConsultaOut)
def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    return delete_consulta_service(db, consulta_id)

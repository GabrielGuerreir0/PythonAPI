# app/services/paciente_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import paciente_model
from app.schemas import paciente_schema


def create_paciente_service(db: Session, paciente: paciente_schema.PacienteCreate):
    db_paciente = paciente_model.Paciente(
        nome=paciente.nome,
        idade=paciente.idade,
        historico_medico=paciente.historico_medico
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente


def get_all_pacientes_service(db: Session):
    return db.query(paciente_model.Paciente).all()


def get_paciente_by_id_service(db: Session, paciente_id: int):
    paciente = db.query(paciente_model.Paciente).filter(paciente_model.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


def update_paciente_service(db: Session, paciente_id: int, paciente: paciente_schema.PacienteCreate):
    db_paciente = db.query(paciente_model.Paciente).filter(paciente_model.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db_paciente.nome = paciente.nome
    db_paciente.idade = paciente.idade
    db_paciente.historico_medico = paciente.historico_medico
    db.commit()
    db.refresh(db_paciente)
    return db_paciente


def delete_paciente_service(db: Session, paciente_id: int):
    db_paciente = db.query(paciente_model.Paciente).filter(paciente_model.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(db_paciente)
    db.commit()
    return db_paciente

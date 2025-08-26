# app/services/medico_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import medico_model
from app.schemas import medico_schema


def create_medico_service(db: Session, medico: medico_schema.MedicoCreate):
    db_medico = medico_model.Medico(nome=medico.nome, especialidade=medico.especialidade)
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico


def get_all_medicos_service(db: Session):
    return db.query(medico_model.Medico).all()


def get_medico_by_id_service(db: Session, medico_id: int):
    medico = db.query(medico_model.Medico).filter(medico_model.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico


def update_medico_service(db: Session, medico_id: int, medico: medico_schema.MedicoCreate):
    db_medico = db.query(medico_model.Medico).filter(medico_model.Medico.id == medico_id).first()
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db_medico.nome = medico.nome
    db_medico.especialidade = medico.especialidade
    db.commit()
    db.refresh(db_medico)
    return db_medico


def delete_medico_service(db: Session, medico_id: int):
    db_medico = db.query(medico_model.Medico).filter(medico_model.Medico.id == medico_id).first()
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db.delete(db_medico)
    db.commit()
    return db_medico

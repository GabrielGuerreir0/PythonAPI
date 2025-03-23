# app/services/consulta_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import consulta_model
from app.schemas import consulta_schema


def create_consulta_service(db: Session, consulta: consulta_schema.ConsultaCreate):
    try:
        db_consulta = consulta_model.Consulta(
            paciente_id=consulta.paciente_id,
            medico_id=consulta.medico_id,
            data=consulta.data,
            hora=consulta.hora,
            descricao=consulta.descricao
        )
        db.add(db_consulta)
        db.commit()
        db.refresh(db_consulta)
        return db_consulta
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar data ou hora: {str(e)}")


def get_all_consultas_service(db: Session):
    return db.query(consulta_model.Consulta).all()


def get_consulta_by_id_service(db: Session, consulta_id: int):
    consulta = db.query(consulta_model.Consulta).filter(consulta_model.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta


def update_consulta_service(db: Session, consulta_id: int, consulta: consulta_schema.ConsultaCreate):
    db_consulta = db.query(consulta_model.Consulta).filter(consulta_model.Consulta.id == consulta_id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    try:
        db_consulta.paciente_id = consulta.paciente_id
        db_consulta.medico_id = consulta.medico_id
        db_consulta.data = consulta.data
        db_consulta.hora = consulta.hora
        db_consulta.descricao = consulta.descricao
        
        db.commit()
        db.refresh(db_consulta)
        return db_consulta
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar data ou hora: {str(e)}")


def delete_consulta_service(db: Session, consulta_id: int):
    db_consulta = db.query(consulta_model.Consulta).filter(consulta_model.Consulta.id == consulta_id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db.delete(db_consulta)
    db.commit()
    return db_consulta

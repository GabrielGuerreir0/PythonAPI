from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal


router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um médico
@router.post("/", response_model=schemas.MedicoOut)
def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = models.Medico(nome=medico.nome, especialidade=medico.especialidade)
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

# Rota para listar todos os médicos
@router.get("/", response_model=list[schemas.MedicoOut])
def get_medicos(db: Session = Depends(get_db)):
    medicos = db.query(models.Medico).all()
    return medicos

# Rota para obter um médico por ID
@router.get("/{medico_id}", response_model=schemas.MedicoOut)
def get_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico

# Rota para atualizar um médico
@router.put("/{medico_id}", response_model=schemas.MedicoOut)
def update_medico(medico_id: int, medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db_medico.nome = medico.nome
    db_medico.especialidade = medico.especialidade
    db.commit()
    db.refresh(db_medico)
    return db_medico

# Rota para deletar um médico
@router.delete("/{medico_id}", response_model=schemas.MedicoOut)
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db.delete(db_medico)
    db.commit()
    return db_medico

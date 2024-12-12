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

# Rota para criar um paciente
@router.post("/", response_model=schemas.PacienteOut)
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(nome=paciente.nome, idade=paciente.idade, historico_medico=paciente.historico_medico)
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Rota para listar todos os pacientes
@router.get("/", response_model=list[schemas.PacienteOut])
def get_pacientes(db: Session = Depends(get_db)):
    pacientes = db.query(models.Paciente).all()
    return pacientes

# Rota para obter um paciente por ID
@router.get("/{paciente_id}", response_model=schemas.PacienteOut)
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

# Rota para atualizar um paciente
@router.put("/{paciente_id}", response_model=schemas.PacienteOut)
def update_paciente(paciente_id: int, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db_paciente.nome = paciente.nome
    db_paciente.idade = paciente.idade
    db_paciente.historico_medico = paciente.historico_medico
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Rota para deletar um paciente
@router.delete("/{paciente_id}", response_model=schemas.PacienteOut)
def delete_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(db_paciente)
    db.commit()
    return db_paciente

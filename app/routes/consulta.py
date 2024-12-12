from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar uma consulta
@router.post("/", response_model=schemas.ConsultaOut)
def create_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = models.Consulta(
        paciente_id=consulta.paciente_id,
        medico_id=consulta.medico_id,
        data=consulta.data,
        horario=consulta.horario
    )
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Rota para listar todas as consultas
@router.get("/", response_model=list[schemas.ConsultaOut])
def get_consultas(db: Session = Depends(get_db)):
    consultas = db.query(models.Consulta).all()
    return consultas

# Rota para obter uma consulta por ID
@router.get("/{consulta_id}", response_model=schemas.ConsultaOut)
def get_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta

# Rota para atualizar uma consulta
@router.put("/{consulta_id}", response_model=schemas.ConsultaOut)
def update_consulta(consulta_id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db_consulta.paciente_id = consulta.paciente_id
    db_consulta.medico_id = consulta.medico_id
    db_consulta.data = consulta.data
    db_consulta.horario = consulta.horario
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Rota para deletar uma consulta
@router.delete("/{consulta_id}", response_model=schemas.ConsultaOut)
def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db.delete(db_consulta)
    db.commit()
    return db_consulta

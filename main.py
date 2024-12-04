from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    historico_medico = Column(String)

class Medico(Base):
    __tablename__ = "medicos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    especialidade = Column(String)

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    data = Column(String)
    hora = Column(String)

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")


Paciente.consultas = relationship("Consulta", back_populates="paciente")
Medico.consultas = relationship("Consulta", back_populates="medico")


Base.metadata.create_all(bind=engine)


app = FastAPI()


class PacienteCreate(BaseModel):
    nome: str
    idade: int
    historico_medico: str

class MedicoCreate(BaseModel):
    nome: str
    especialidade: str

class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    data: str
    hora: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD para Pacientes
@app.get("/pacientes", response_model=List[PacienteCreate], tags=["Paciente"])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()

@app.post("/pacientes", response_model=PacienteCreate, tags=["Paciente"])
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.put("/pacientes/{paciente_id}", response_model=PacienteCreate, tags=["Paciente"])
def atualizar_paciente(paciente_id: int, paciente: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    for key, value in paciente.dict().items():
        setattr(db_paciente, key, value)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.delete("/pacientes/{paciente_id}", response_model=PacienteCreate, tags=["Paciente"])
def deletar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(db_paciente)
    db.commit()
    return db_paciente

# CRUD para Médicos
@app.get("/medicos", response_model=List[MedicoCreate], tags=["Medico"])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(Medico).all()

@app.post("/medicos", response_model=MedicoCreate, tags=["Medico"])
def criar_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    db_medico = Medico(**medico.dict())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

@app.put("/medicos/{medico_id}", response_model=MedicoCreate, tags=["Medico"])
def atualizar_medico(medico_id: int, medico: MedicoCreate, db: Session = Depends(get_db)):
    db_medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    for key, value in medico.dict().items():
        setattr(db_medico, key, value)
    db.commit()
    db.refresh(db_medico)
    return db_medico

@app.delete("/medicos/{medico_id}", response_model=MedicoCreate, tags=["Medico"])
def deletar_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    db.delete(db_medico)
    db.commit()
    return db_medico

# CRUD para Consultas
@app.get("/consultas", response_model=List[ConsultaCreate], tags=["Consulta"])
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(Consulta).all()

@app.post("/consultas", response_model=ConsultaCreate, tags=["Consulta"])
def criar_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@app.put("/consultas/{consulta_id}", response_model=ConsultaCreate, tags=["Consulta"])
def atualizar_consulta(consulta_id: int, consulta: ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    for key, value in consulta.dict().items():
        setattr(db_consulta, key, value)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@app.delete("/consultas/{consulta_id}", response_model=ConsultaCreate, tags=["Consulta"])
def deletar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    db.delete(db_consulta)
    db.commit()
    return db_consulta

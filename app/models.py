from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class Paciente(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    historico_medico = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    # Relacionamento com Consulta
    consultas = relationship(
        "Consulta",
        back_populates="paciente",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Paciente(nome={self.nome}, idade={self.idade})>"


class Medico(Base):
    __tablename__ = 'medicos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    # Relacionamento com Consulta
    consultas = relationship(
        "Consulta",
        back_populates="medico",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Medico(nome={self.nome}, especialidade={self.especialidade})>"


class Consulta(Base):
    __tablename__ = 'consultas'

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    descricao = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    # Relacionamentos com Paciente e Medico
    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")

    def __repr__(self):
        return f"<Consulta(data={self.data}, hora={self.hora}, paciente_id={self.paciente_id}, medico_id={self.medico_id})>"

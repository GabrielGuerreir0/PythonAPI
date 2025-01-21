from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Paciente(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    historico_medico = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    consultas = relationship("Consulta", back_populates="paciente")  # Relacionamento explícito


class Medico(Base):
    __tablename__ = 'medicos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    consultas = relationship("Consulta", back_populates="medico")  # Relacionamento explícito


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

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")

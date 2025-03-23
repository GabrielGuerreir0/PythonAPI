from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Paciente(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    historico_medico = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    consultas = relationship("Consulta", back_populates="paciente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paciente(nome={self.nome}, idade={self.idade})>"

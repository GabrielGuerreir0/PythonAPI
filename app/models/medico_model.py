from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Medico(Base):
    __tablename__ = 'medicos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    consultas = relationship("Consulta", back_populates="medico", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Medico(nome={self.nome}, especialidade={self.especialidade})>"

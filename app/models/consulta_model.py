from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

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

    def __repr__(self):
        return f"<Consulta(data={self.data}, hora={self.hora}, paciente_id={self.paciente_id}, medico_id={self.medico_id})>"

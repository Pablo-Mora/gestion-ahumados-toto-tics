from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class WebAccess(Base):
    __tablename__ = "web_accesses"

    id = Column(Integer, primary_key=True, index=True)
    nombre_servicio = Column(String, index=True, nullable=False)
    url = Column(String, nullable=True) # Store as String, Pydantic handles HttpUrl validation
    usuario = Column(String, nullable=False)
    hashed_contrasena = Column(String, nullable=False) # Store the hash of the password
    descripcion = Column(Text, nullable=True)
    notas_adicionales = Column(Text, nullable=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    # Relationship
    employee = relationship("Employee", back_populates="web_accesses")

    def __repr__(self):
        return f"<WebAccess(id={self.id}, nombre_servicio='{self.nombre_servicio}', user='{self.usuario}')>"

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from app.auth.models import User # Import User model for relationships
from typing import Optional # For Mapped type hints

class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    software_nombre = Column(String, index=True, nullable=False)
    fabricante = Column(String, nullable=True)
    clave_producto = Column(String, nullable=True) # Consider encryption for sensitive keys
    tipo_licencia = Column(String, nullable=False)
    cantidad_usuarios = Column(Integer, default=1)
    fecha_compra = Column(Date, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    proveedor = Column(String, nullable=True)
    costo = Column(Float, nullable=True)
    notas = Column(Text, nullable=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    hardware_id = Column(Integer, ForeignKey("hardware.id"), nullable=True)

    # Relationships
    employee = relationship("Employee", back_populates="licenses")
    hardware = relationship("Hardware", back_populates="licenses")

    # Delivery and Approval Information
    entregado_por_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    aprobado_por_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    fecha_entrega: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    fecha_aprobacion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)

    entregado_por: Mapped[Optional["User"]] = relationship("User", foreign_keys=[entregado_por_id], lazy="selectin")
    aprobado_por: Mapped[Optional["User"]] = relationship("User", foreign_keys=[aprobado_por_id], lazy="selectin")

    def __repr__(self):
        return f"<License(id={self.id}, software_nombre='{self.software_nombre}', tipo='{self.tipo_licencia}')>"

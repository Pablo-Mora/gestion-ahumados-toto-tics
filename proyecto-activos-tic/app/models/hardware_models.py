from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base # Import Base from the central database.py
from app.auth.models import User # Import User model for relationships
from typing import Optional # For Mapped type hints

class Hardware(Base):
    __tablename__ = "hardware"

    id = Column(Integer, primary_key=True, index=True)
    tipo_equipo = Column(String, index=True, nullable=False)
    marca = Column(String, index=True, nullable=False)
    modelo = Column(String, nullable=True)
    serial = Column(String, unique=True, index=True, nullable=False)
    numero_activo = Column(String, unique=True, nullable=True, index=True) # Company asset number
    estado = Column(String, default="operativo") # e.g., operativo, en reparación, de baja
    ubicacion_actual = Column(String, nullable=True)
    fecha_compra = Column(Date, nullable=True)
    proveedor = Column(String, nullable=True)
    costo = Column(Float, nullable=True)
    notas = Column(Text, nullable=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True) # Foreign key to Employee

    # Relationship to the Employee model
    # This means a Hardware item can be linked to one Employee
    employee = relationship("Employee", back_populates="hardware_items")

    # Relationship for licenses associated with this hardware item (e.g., OEM licenses)
    licenses = relationship(
        "License",
        back_populates="hardware",
        cascade="all, delete-orphan" # If hardware is deleted, its licenses might be unassigned or deleted
    )

    # Delivery and Approval Information
    entregado_por_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    aprobado_por_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    fecha_entrega: Mapped[Optional[Date]] = mapped_column(Date, nullable=True) # Using Date directly from sqlalchemy
    fecha_aprobacion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True) # Using Date directly from sqlalchemy

    entregado_por: Mapped[Optional["User"]] = relationship("User", foreign_keys=[entregado_por_id], lazy="selectin")
    aprobado_por: Mapped[Optional["User"]] = relationship("User", foreign_keys=[aprobado_por_id], lazy="selectin")


    def __repr__(self):
        return f"<Hardware(id={self.id}, tipo='{self.tipo_equipo}', serial='{self.serial}')>"

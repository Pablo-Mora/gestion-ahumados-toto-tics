from sqlalchemy import Column, Integer, String, ForeignKey # ForeignKey will be used later
from sqlalchemy.orm import relationship
from app.database import Base # Import Base from the central database.py

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    identificacion = Column(String, unique=True, index=True, nullable=False)
    cargo = Column(String, index=True, nullable=False)
    departamento = Column(String, nullable=True)
    ubicacion_oficina = Column(String, nullable=True)
    telefono_contacto = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True) # Assuming email should be unique if provided

    # Relationship for hardware items assigned to this employee
    # Will be a list of Hardware objects
    hardware_items = relationship(
        "Hardware",
        back_populates="employee",
        cascade="all, delete-orphan" # If employee is deleted, their hardware associations might be handled or cleared
    )

    # Relationship for licenses assigned to this employee
    licenses = relationship(
        "License",
        back_populates="employee",
        cascade="all, delete-orphan" # If employee is deleted, their licenses might be unassigned or deleted
    )

    # Relationship for web access credentials assigned to this employee
    web_accesses = relationship(
        "WebAccess",
        back_populates="employee",
        cascade="all, delete-orphan" # If employee is deleted, their web accesses are also deleted
    )

    def __repr__(self):
        return f"<Employee(id={self.id}, nombre='{self.nombre}', identificacion='{self.identificacion}', cargo='{self.cargo}')>"

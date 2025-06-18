from pydantic import BaseModel
from typing import Optional, List
from datetime import date # For fields like purchase_date

# Forward reference for Employee schema if needed for detailed responses
# class EmployeeBasicInfo(BaseModel):
#     id: int
#     nombre: str
#     class Config:
#         orm_mode = True

class HardwareBase(BaseModel):
    tipo_equipo: str # e.g., Laptop, Desktop, Monitor, Teclado, Mouse
    marca: str
    modelo: Optional[str] = None
    serial: str # Should be unique
    numero_activo: Optional[str] = None # Asset number if used by company
    estado: Optional[str] = "operativo" # e.g., operativo, en reparación, de baja
    ubicacion_actual: Optional[str] = None # Specific office, desk, or storage
    fecha_compra: Optional[date] = None
    proveedor: Optional[str] = None
    costo: Optional[float] = None
    notas: Optional[str] = None
    # Delivery and Approval fields
    entregado_por_id: Optional[int] = None
    aprobado_por_id: Optional[int] = None
    fecha_entrega: Optional[date] = None
    fecha_aprobacion: Optional[date] = None

class HardwareCreate(HardwareBase):
    employee_id: Optional[int] = None # For assigning to an employee upon creation
    # entregado_por_id, etc., can be set via HardwareUpdate or a dedicated route later if needed initially

class HardwareUpdate(HardwareBase):
    tipo_equipo: Optional[str] = None
    marca: Optional[str] = None
    serial: Optional[str] = None # Usually serial numbers don't change, but allow if needed
    numero_activo: Optional[str] = None
    estado: Optional[str] = None
    ubicacion_actual: Optional[str] = None
    fecha_compra: Optional[date] = None
    proveedor: Optional[str] = None
    costo: Optional[float] = None
    notas: Optional[str] = None
    employee_id: Optional[int] = None # To change or assign employee
    # Delivery and Approval fields for update
    entregado_por_id: Optional[int] = None
    aprobado_por_id: Optional[int] = None
    fecha_entrega: Optional[date] = None
    fecha_aprobacion: Optional[date] = None

class Hardware(HardwareBase):
    id: int
    employee_id: Optional[int] = None
    from .employee_schemas import EmployeeBase # Using EmployeeBase to avoid circular dependency with full Employee
    employee: Optional[EmployeeBase] = None

    class Config:
        orm_mode = True

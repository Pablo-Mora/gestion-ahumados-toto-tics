from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Forward reference for Employee and Hardware schemas if needed for detailed responses
# class EmployeeBasicInfo(BaseModel):
#     id: int
#     nombre: str
#     class Config:
#         orm_mode = True

# class HardwareBasicInfo(BaseModel):
#     id: int
#     serial: str
#     class Config:
#         orm_mode = True

class LicenseBase(BaseModel):
    software_nombre: str
    fabricante: Optional[str] = None
    clave_producto: Optional[str] = None # Product key, might be sensitive
    tipo_licencia: str # e.g., "Perpetua", "Suscripción Anual", "Suscripción Mensual", "OEM"
    cantidad_usuarios: Optional[int] = 1 # Number of users/devices this license covers
    fecha_compra: Optional[date] = None
    fecha_vencimiento: Optional[date] = None # Especially for subscriptions
    proveedor: Optional[str] = None
    costo: Optional[float] = None
    notas: Optional[str] = None
    # Delivery and Approval fields
    entregado_por_id: Optional[int] = None
    aprobado_por_id: Optional[int] = None
    fecha_entrega: Optional[date] = None
    fecha_aprobacion: Optional[date] = None

class LicenseCreate(LicenseBase):
    employee_id: Optional[int] = None # For assigning to an employee
    hardware_id: Optional[int] = None # For assigning to a specific hardware item (e.g., OEM license)
    # Delivery/approval fields can be set via Update or dedicated route if needed at creation

class LicenseUpdate(LicenseBase):
    software_nombre: Optional[str] = None
    tipo_licencia: Optional[str] = None
    # All other fields are optional for update
    employee_id: Optional[int] = None
    hardware_id: Optional[int] = None
    # Delivery and Approval fields for update
    entregado_por_id: Optional[int] = None
    aprobado_por_id: Optional[int] = None
    fecha_entrega: Optional[date] = None
    fecha_aprobacion: Optional[date] = None


class License(LicenseBase):
    id: int
    # employee_id, hardware_id, and delivery/approval fields are inherited from LicenseBase

    from .employee_schemas import EmployeeBase # Using EmployeeBase to avoid circular dependency
    from .hardware_schemas import HardwareBase # Using HardwareBase to avoid circular dependency

    employee: Optional[EmployeeBase] = None
    hardware: Optional[HardwareBase] = None
    # We could add schemas for UserBase to show entregado_por and aprobado_por details if desired

    class Config:
        orm_mode = True

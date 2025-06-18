from pydantic import BaseModel, EmailStr # EmailStr for email validation if needed later
from typing import Optional, List # List will be used for related items

# Forward references for related schemas if needed later, e.g., Hardware, License
# class Hardware(BaseModel): # Simplified, actual import later
#     id: int
#     serial: str
#     class Config:
#         orm_mode = True

# class License(BaseModel): # Simplified, actual import later
#     id: int
#     software_name: str
#     class Config:
#         orm_mode = True

class EmployeeBase(BaseModel):
    nombre: str
    identificacion: str # Could add validation, e.g., regex
    cargo: str
    departamento: Optional[str] = None
    ubicacion_oficina: Optional[str] = None
    telefono_contacto: Optional[str] = None
    email: Optional[EmailStr] = None # Using EmailStr for validation

class EmployeeCreate(EmployeeBase):
    pass # No extra fields for creation beyond base for now

class EmployeeUpdate(EmployeeBase):
    nombre: Optional[str] = None
    identificacion: Optional[str] = None
    cargo: Optional[str] = None
    # All fields are optional for update

class Employee(EmployeeBase):
    id: int
    from .hardware_schemas import Hardware as HardwareSchema # Alias to avoid naming conflict
    from .license_schemas import License as LicenseSchema # Alias
    from .web_access_schemas import WebAccess as WebAccessSchema # Alias

    hardware_items: List[HardwareSchema] = []
    licenses: List[LicenseSchema] = []
    web_accesses: List[WebAccessSchema] = []

    class Config:
        orm_mode = True # To allow mapping from SQLAlchemy models

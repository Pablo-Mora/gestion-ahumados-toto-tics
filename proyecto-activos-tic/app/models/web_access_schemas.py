from pydantic import BaseModel, HttpUrl
from typing import Optional

# class EmployeeBasicInfo(BaseModel): # Forward reference if needed
#     id: int
#     nombre: str
#     class Config:
#         orm_mode = True

class WebAccessBase(BaseModel):
    nombre_servicio: str # e.g., "Company VPN", "Internal HR Portal", "Cloud Provider Console"
    url: Optional[HttpUrl] = None # Validate as URL
    usuario: str
    # NOTE: Storing plain passwords is a security risk.
    # Consider using a dedicated secrets manager or client-side encryption.
    # For this example, password_placeholder is used for creation/update,
    # but it won't be stored directly if hashed in the model.
    # The `WebAccess` response schema will omit the password.
    descripcion: Optional[str] = None
    notas_adicionales: Optional[str] = None

class WebAccessCreate(WebAccessBase):
    password_placeholder: str # To be hashed by the backend, not stored as is
    employee_id: int # Must be assigned to an employee

class WebAccessUpdate(WebAccessBase):
    nombre_servicio: Optional[str] = None
    usuario: Optional[str] = None
    password_placeholder: Optional[str] = None # For updating the password
    employee_id: Optional[int] = None # To reassign if necessary
    # All fields are optional for update

class WebAccess(WebAccessBase):
    id: int
    employee_id: int
    from .employee_schemas import EmployeeBase # Using EmployeeBase to avoid circular dependency
    employee: Optional[EmployeeBase] = None

    # IMPORTANT: Exclude password from being returned in API responses
    # This is handled by not including 'password_placeholder' or 'hashed_contrasena' here.
    # If 'hashed_contrasena' were part of WebAccessBase and returned, it would be a leak.

    class Config:
        orm_mode = True

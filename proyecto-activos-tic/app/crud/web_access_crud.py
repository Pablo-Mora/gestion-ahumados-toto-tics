from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import web_access_models
from app.models import web_access_schemas
from app.auth.auth import get_password_hash # For hashing passwords

def get_web_access(db: Session, web_access_id: int) -> Optional[web_access_models.WebAccess]:
    return db.query(web_access_models.WebAccess).filter(web_access_models.WebAccess.id == web_access_id).first()

def get_web_accesses_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[web_access_models.WebAccess]:
    return db.query(web_access_models.WebAccess).filter(web_access_models.WebAccess.employee_id == employee_id).offset(skip).limit(limit).all()

def get_all_web_accesses(db: Session, skip: int = 0, limit: int = 100) -> List[web_access_models.WebAccess]: # If admin needs to see all
    return db.query(web_access_models.WebAccess).offset(skip).limit(limit).all()

def create_web_access(db: Session, web_access: web_access_schemas.WebAccessCreate) -> web_access_models.WebAccess:
    hashed_password = get_password_hash(web_access.password_placeholder)
    db_web_access = web_access_models.WebAccess(
        nombre_servicio=web_access.nombre_servicio,
        url=str(web_access.url) if web_access.url else None, # Ensure URL is string or None
        usuario=web_access.usuario,
        hashed_contrasena=hashed_password,
        descripcion=web_access.descripcion,
        notas_adicionales=web_access.notas_adicionales,
        employee_id=web_access.employee_id
    )
    db.add(db_web_access)
    db.commit()
    db.refresh(db_web_access)
    return db_web_access

def update_web_access(db: Session, web_access_id: int, web_access_update: web_access_schemas.WebAccessUpdate) -> Optional[web_access_models.WebAccess]:
    db_web_access = get_web_access(db, web_access_id)
    if db_web_access:
        update_data = web_access_update.dict(exclude_unset=True)

        if "password_placeholder" in update_data and update_data["password_placeholder"] is not None:
            hashed_password = get_password_hash(update_data["password_placeholder"])
            db_web_access.hashed_contrasena = hashed_password
            del update_data["password_placeholder"] # Don't try to set this attribute directly

        if "url" in update_data and update_data["url"] is not None:
            update_data["url"] = str(update_data["url"])

        for key, value in update_data.items():
            setattr(db_web_access, key, value)

        db.commit()
        db.refresh(db_web_access)
    return db_web_access

def delete_web_access(db: Session, web_access_id: int) -> Optional[web_access_models.WebAccess]:
    db_web_access = get_web_access(db, web_access_id)
    if db_web_access:
        db.delete(db_web_access)
        db.commit()
    return db_web_access

from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import license_models
from app.models import license_schemas

def get_license(db: Session, license_id: int) -> Optional[license_models.License]:
    return db.query(license_models.License).filter(license_models.License.id == license_id).first()

def get_licenses(db: Session, skip: int = 0, limit: int = 100) -> List[license_models.License]:
    return db.query(license_models.License).offset(skip).limit(limit).all()

def create_license(db: Session, license: license_schemas.LicenseCreate) -> license_models.License:
    # employee_id and hardware_id are part of LicenseCreate schema
    db_license = license_models.License(**license.dict())
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

def update_license(db: Session, license_id: int, license_update: license_schemas.LicenseUpdate) -> Optional[license_models.License]:
    db_license = get_license(db, license_id)
    if db_license:
        update_data = license_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_license, key, value)
        db.commit()
        db.refresh(db_license)
    return db_license

def delete_license(db: Session, license_id: int) -> Optional[license_models.License]:
    db_license = get_license(db, license_id)
    if db_license:
        db.delete(db_license)
        db.commit()
    return db_license

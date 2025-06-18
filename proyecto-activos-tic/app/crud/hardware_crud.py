from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import hardware_models
from app.models import hardware_schemas

def get_hardware_item(db: Session, hardware_id: int) -> Optional[hardware_models.Hardware]:
    return db.query(hardware_models.Hardware).filter(hardware_models.Hardware.id == hardware_id).first()

def get_hardware_by_serial(db: Session, serial: str) -> Optional[hardware_models.Hardware]:
    return db.query(hardware_models.Hardware).filter(hardware_models.Hardware.serial == serial).first()

def get_hardware_items(db: Session, skip: int = 0, limit: int = 100) -> List[hardware_models.Hardware]:
    return db.query(hardware_models.Hardware).offset(skip).limit(limit).all()

def create_hardware_item(db: Session, hardware: hardware_schemas.HardwareCreate) -> hardware_models.Hardware:
    # employee_id is part of HardwareCreate schema and will be passed in hardware.dict()
    db_hardware = hardware_models.Hardware(**hardware.dict())
    db.add(db_hardware)
    db.commit()
    db.refresh(db_hardware)
    return db_hardware

def update_hardware_item(db: Session, hardware_id: int, hardware_update: hardware_schemas.HardwareUpdate) -> Optional[hardware_models.Hardware]:
    db_hardware = get_hardware_item(db, hardware_id)
    if db_hardware:
        update_data = hardware_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_hardware, key, value)
        db.commit()
        db.refresh(db_hardware)
    return db_hardware

def delete_hardware_item(db: Session, hardware_id: int) -> Optional[hardware_models.Hardware]:
    db_hardware = get_hardware_item(db, hardware_id)
    if db_hardware:
        db.delete(db_hardware)
        db.commit()
    return db_hardware

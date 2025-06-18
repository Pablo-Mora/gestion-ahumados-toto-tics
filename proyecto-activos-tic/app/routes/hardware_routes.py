from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import hardware_crud
from app.models import hardware_schemas
from app.auth import auth # For authentication dependency
from app.auth import models as auth_models # For type hinting current_user

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"],
    dependencies=[Depends(auth.get_current_active_user)] # Apply auth to all routes
)

@router.post("/", response_model=hardware_schemas.Hardware, status_code=status.HTTP_201_CREATED)
def create_hardware_item_route(
    hardware: hardware_schemas.HardwareCreate,
    db: Session = Depends(get_db)
):
    db_hardware_by_serial = hardware_crud.get_hardware_by_serial(db, serial=hardware.serial)
    if db_hardware_by_serial:
        raise HTTPException(status_code=400, detail=f"Hardware with serial number {hardware.serial} already exists.")
    # Add other unique checks if necessary, e.g., for numero_activo
    return hardware_crud.create_hardware_item(db=db, hardware=hardware)

@router.get("/", response_model=List[hardware_schemas.Hardware])
def read_hardware_items_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    hardware_items = hardware_crud.get_hardware_items(db, skip=skip, limit=limit)
    return hardware_items

@router.get("/{hardware_id}", response_model=hardware_schemas.Hardware)
def read_hardware_item_route(hardware_id: int, db: Session = Depends(get_db)):
    db_hardware = hardware_crud.get_hardware_item(db, hardware_id=hardware_id)
    if db_hardware is None:
        raise HTTPException(status_code=404, detail="Hardware item not found")
    return db_hardware

@router.put("/{hardware_id}", response_model=hardware_schemas.Hardware)
def update_hardware_item_route(
    hardware_id: int,
    hardware_update: hardware_schemas.HardwareUpdate,
    db: Session = Depends(get_db)
):
    db_hardware = hardware_crud.get_hardware_item(db, hardware_id=hardware_id)
    if db_hardware is None:
        raise HTTPException(status_code=404, detail="Hardware item not found")

    # Check if new 'serial' is being set and if it conflicts
    if hardware_update.serial and hardware_update.serial != db_hardware.serial:
        conflicting_hardware = hardware_crud.get_hardware_by_serial(db, serial=hardware_update.serial)
        if conflicting_hardware:
            raise HTTPException(status_code=400, detail=f"Another hardware item with serial {hardware_update.serial} already exists.")

    # Add other unique field conflict checks if necessary (e.g. numero_activo)

    updated_hardware = hardware_crud.update_hardware_item(db=db, hardware_id=hardware_id, hardware_update=hardware_update)
    return updated_hardware

@router.delete("/{hardware_id}", status_code=status.HTTP_200_OK) # Or 204 No Content
def delete_hardware_item_route(hardware_id: int, db: Session = Depends(get_db)):
    db_hardware = hardware_crud.get_hardware_item(db, hardware_id=hardware_id)
    if db_hardware is None:
        raise HTTPException(status_code=404, detail="Hardware item not found")
    hardware_crud.delete_hardware_item(db=db, hardware_id=hardware_id)
    return {"message": "Hardware item deleted successfully", "hardware_id": hardware_id} # Or just status 204

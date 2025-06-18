from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import license_crud
from app.models import license_schemas
from app.auth import auth # For authentication dependency

router = APIRouter(
    prefix="/licenses",
    tags=["Licenses"],
    dependencies=[Depends(auth.get_current_active_user)]
)

@router.post("/", response_model=license_schemas.License, status_code=status.HTTP_201_CREATED)
def create_license_route(
    license_in: license_schemas.LicenseCreate, # Renamed to avoid conflict
    db: Session = Depends(get_db)
):
    # Add any specific validation if needed, e.g., check if employee_id or hardware_id exist
    return license_crud.create_license(db=db, license=license_in)

@router.get("/", response_model=List[license_schemas.License])
def read_licenses_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    licenses = license_crud.get_licenses(db, skip=skip, limit=limit)
    return licenses

@router.get("/{license_id}", response_model=license_schemas.License)
def read_license_route(license_id: int, db: Session = Depends(get_db)):
    db_license = license_crud.get_license(db, license_id=license_id)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return db_license

@router.put("/{license_id}", response_model=license_schemas.License)
def update_license_route(
    license_id: int,
    license_in: license_schemas.LicenseUpdate, # Renamed
    db: Session = Depends(get_db)
):
    db_license = license_crud.get_license(db, license_id=license_id)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    updated_license = license_crud.update_license(db=db, license_id=license_id, license_update=license_in)
    return updated_license

@router.delete("/{license_id}", status_code=status.HTTP_200_OK)
def delete_license_route(license_id: int, db: Session = Depends(get_db)):
    db_license = license_crud.get_license(db, license_id=license_id)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    license_crud.delete_license(db=db, license_id=license_id)
    return {"message": "License deleted successfully", "license_id": license_id}

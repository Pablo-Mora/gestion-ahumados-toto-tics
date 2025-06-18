from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import employee_crud
from app.models import employee_schemas
from app.auth import auth # For authentication dependency
from app.auth import models as auth_models # For type hinting current_user

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(auth.get_current_active_user)] # Apply auth to all routes in this router
)

@router.post("/", response_model=employee_schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee_route(
    employee: employee_schemas.EmployeeCreate,
    db: Session = Depends(get_db)
    # current_user: auth_models.User = Depends(auth.get_current_active_user) # Already covered by router dependency
):
    db_employee_by_id = employee_crud.get_employee_by_identificacion(db, identificacion=employee.identificacion)
    if db_employee_by_id:
        raise HTTPException(status_code=400, detail=f"Employee with identificacion {employee.identificacion} already exists.")
    if employee.email: # Check if email is provided and if it already exists
        # This assumes you'll add a get_employee_by_email to employee_crud if strict email uniqueness is needed
        # For now, we'll skip this check or assume identificacion is primary unique business key for employees
        pass
    return employee_crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=List[employee_schemas.Employee])
def read_employees_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    employees = employee_crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.get("/{employee_id}", response_model=employee_schemas.Employee)
def read_employee_route(employee_id: int, db: Session = Depends(get_db)):
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=employee_schemas.Employee)
def update_employee_route(
    employee_id: int,
    employee_update: employee_schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if new 'identificacion' is being set and if it conflicts with another employee
    if employee_update.identificacion and employee_update.identificacion != db_employee.identificacion:
        conflicting_employee = employee_crud.get_employee_by_identificacion(db, identificacion=employee_update.identificacion)
        if conflicting_employee:
            raise HTTPException(status_code=400, detail=f"Another employee with identificacion {employee_update.identificacion} already exists.")

    updated_employee = employee_crud.update_employee(db=db, employee_id=employee_id, employee_update=employee_update)
    return updated_employee

@router.delete("/{employee_id}", status_code=status.HTTP_200_OK) # Or 204 No Content
def delete_employee_route(employee_id: int, db: Session = Depends(get_db)):
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_crud.delete_employee(db=db, employee_id=employee_id)
    return {"message": "Employee deleted successfully", "employee_id": employee_id} # Or just status 204

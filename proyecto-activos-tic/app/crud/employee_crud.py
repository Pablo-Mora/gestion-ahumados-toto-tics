from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import employee_models
from app.models import employee_schemas

def get_employee(db: Session, employee_id: int) -> Optional[employee_models.Employee]:
    return db.query(employee_models.Employee).filter(employee_models.Employee.id == employee_id).first()

def get_employee_by_identificacion(db: Session, identificacion: str) -> Optional[employee_models.Employee]:
    return db.query(employee_models.Employee).filter(employee_models.Employee.identificacion == identificacion).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[employee_models.Employee]:
    return db.query(employee_models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: employee_schemas.EmployeeCreate) -> employee_models.Employee:
    db_employee = employee_models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee_update: employee_schemas.EmployeeUpdate) -> Optional[employee_models.Employee]:
    db_employee = get_employee(db, employee_id)
    if db_employee:
        update_data = employee_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int) -> Optional[employee_models.Employee]:
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee

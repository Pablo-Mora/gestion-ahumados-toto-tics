from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import web_access_crud
from app.models import web_access_schemas
from app.auth import auth # For authentication dependency
from app.auth.models import User as AuthUser # For type hinting current_user if needed

router = APIRouter(
    prefix="/web-accesses",
    tags=["Web Accesses"],
    dependencies=[Depends(auth.get_current_active_user)]
)

@router.post("/", response_model=web_access_schemas.WebAccess, status_code=status.HTTP_201_CREATED)
def create_web_access_route(
    web_access_in: web_access_schemas.WebAccessCreate,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(auth.get_current_active_user) # Get current user
):
    # Ensure employee_id in web_access_in matches current_user.id or current_user is admin
    # For simplicity now, we allow creating for employee_id specified in payload if it's valid.
    # A stricter check could be:
    # if current_user.role != "ADMIN" and web_access_in.employee_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to create web access for another user")

    # TODO: Check if employee_id from web_access_in.employee_id exists using employee_crud.get_employee
    # if not employee_crud.get_employee(db, web_access_in.employee_id):
    #     raise HTTPException(status_code=404, detail=f"Employee with id {web_access_in.employee_id} not found.")

    return web_access_crud.create_web_access(db=db, web_access=web_access_in)

@router.get("/", response_model=List[web_access_schemas.WebAccess])
def read_all_web_accesses_route( # Changed from get_web_accesses to get_all_web_accesses
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
    # current_user: AuthUser = Depends(auth.get_current_admin_user) # Example: Only admin can see all
):
    # If only users should see their own, this would be different:
    # web_accesses = web_access_crud.get_web_accesses_by_employee(db, employee_id=current_user.id, skip=skip, limit=limit)
    web_accesses = web_access_crud.get_all_web_accesses(db, skip=skip, limit=limit)
    return web_accesses

@router.get("/by-employee/{employee_id}", response_model=List[web_access_schemas.WebAccess])
def read_web_accesses_for_employee_route(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(auth.get_current_active_user)
):
    if current_user.role != "ADMIN" and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Not authorized to view web accesses for this employee.")

    # TODO: Check if employee_id exists
    # if not employee_crud.get_employee(db, employee_id):
    #     raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found.")

    web_accesses = web_access_crud.get_web_accesses_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)
    if not web_accesses:
        # Return empty list if none found, or 404 if employee has no web accesses at all (depends on desired behavior)
        pass # HTTPException(status_code=404, detail="No web accesses found for this employee")
    return web_accesses


@router.get("/{web_access_id}", response_model=web_access_schemas.WebAccess)
def read_web_access_route(
    web_access_id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(auth.get_current_active_user)
):
    db_web_access = web_access_crud.get_web_access(db, web_access_id=web_access_id)
    if db_web_access is None:
        raise HTTPException(status_code=404, detail="Web access not found")
    if current_user.role != "ADMIN" and db_web_access.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this web access")
    return db_web_access

@router.put("/{web_access_id}", response_model=web_access_schemas.WebAccess)
def update_web_access_route(
    web_access_id: int,
    web_access_in: web_access_schemas.WebAccessUpdate,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(auth.get_current_active_user)
):
    db_web_access = web_access_crud.get_web_access(db, web_access_id=web_access_id)
    if db_web_access is None:
        raise HTTPException(status_code=404, detail="Web access not found")
    if current_user.role != "ADMIN" and db_web_access.employee_id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to update this web access")

    # If employee_id is being changed, only admin should be allowed to assign to a *different* employee
    if web_access_in.employee_id is not None and web_access_in.employee_id != db_web_access.employee_id:
        if current_user.role != "ADMIN":
            raise HTTPException(status_code=403, detail="Only admins can reassign web access to a different employee.")
        # TODO: Check if new employee_id exists
        # if not employee_crud.get_employee(db, web_access_in.employee_id):
        #     raise HTTPException(status_code=404, detail=f"Target employee with id {web_access_in.employee_id} not found.")

    updated_web_access = web_access_crud.update_web_access(db=db, web_access_id=web_access_id, web_access_update=web_access_in)
    return updated_web_access

@router.delete("/{web_access_id}", status_code=status.HTTP_200_OK)
def delete_web_access_route(
    web_access_id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(auth.get_current_active_user)
):
    db_web_access = web_access_crud.get_web_access(db, web_access_id=web_access_id)
    if db_web_access is None:
        raise HTTPException(status_code=404, detail="Web access not found")
    if current_user.role != "ADMIN" and db_web_access.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this web access")

    web_access_crud.delete_web_access(db=db, web_access_id=web_access_id)
    return {"message": "Web access deleted successfully", "web_access_id": web_access_id}

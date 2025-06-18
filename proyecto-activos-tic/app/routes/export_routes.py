from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils import export_utils
from app.auth import auth # For authentication dependency
import os

router = APIRouter(
    prefix="/export",
    tags=["Export"],
    dependencies=[Depends(auth.get_current_active_user)]
)

EXPORTS_DIR = "exports" # Define once if not already via export_utils

@router.get("/excel/reporte_activos", response_class=FileResponse)
async def export_inventory_report_excel(db: Session = Depends(get_db)):
    """
    Generates and downloads an Excel report of all IT assets.
    """
    try:
        file_path = export_utils.generate_excel_report(db)

        if not os.path.exists(file_path): # Should not happen if generate_excel_report raises error on failure
            raise HTTPException(status_code=404, detail="Generated Excel report file not found.")

        filename_for_download = os.path.basename(file_path)

        return FileResponse(
            path=file_path,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=filename_for_download
        )
    except Exception as e:
        print(f"Error during Excel report generation or file serving: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate or serve the Excel report: {str(e)}")

@router.get("/word/acta_empleado/{employee_id}", response_class=FileResponse)
async def export_employee_acta_word(employee_id: int, db: Session = Depends(get_db)):
    """
    Generates and downloads a Word document "Acta de Entrega" for a specific employee.
    """
    try:
        # Fetch employee details to get a proper filename, e.g., employee's name or identificacion
        # This is already handled within generate_word_acta for the file path.
        # We need to ensure the employee exists before attempting to generate.
        from app.crud import employee_crud # Local import to avoid top-level circularity if any
        employee = employee_crud.get_employee(db, employee_id=employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found.")

        file_path = export_utils.generate_word_acta(db, employee_id) # Path includes identificacion

        if file_path is None or not os.path.exists(file_path):
            # This case should ideally be handled by an exception within generate_word_acta
            # or by the employee check above.
            raise HTTPException(status_code=404, detail="Generated Word acta file not found or employee does not exist.")

        filename_for_download = os.path.basename(file_path) # e.g., acta_entrega_xxxx.docx

        return FileResponse(
            path=file_path,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=filename_for_download
        )
    except HTTPException as he: # Re-raise HTTPExceptions to let FastAPI handle them
        raise he
    except Exception as e:
        print(f"Error during Word acta generation or file serving: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate or serve the Word acta: {str(e)}")

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io # For BytesIO

from app.database import get_db
from app.analysis import analysis_utils
from app.auth import auth # For authentication dependency

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
    dependencies=[Depends(auth.get_current_active_user)]
)

@router.get("/charts/activos_por_tipo", response_class=StreamingResponse)
async def get_activos_por_tipo_chart(db: Session = Depends(get_db)):
    """
    Generates and returns a PNG image chart of hardware assets grouped by type.
    """
    plot_buffer = analysis_utils.plot_activos_por_tipo(db)

    # Ensure buffer is of type BytesIO, otherwise StreamingResponse might have issues
    if not isinstance(plot_buffer, io.BytesIO):
        # This case should ideally not happen if plot_activos_por_tipo is correct
        # but as a fallback, convert if it's bytes
        if isinstance(plot_buffer, bytes):
            plot_buffer = io.BytesIO(plot_buffer)
        else:
            # Handle error: unexpected buffer type
            raise ValueError("Plot generation returned an unexpected buffer type.") # pragma: no cover

    return StreamingResponse(plot_buffer, media_type="image/png")


@router.get("/charts/empleados_por_departamento", response_class=StreamingResponse)
async def get_empleados_por_departamento_chart(db: Session = Depends(get_db)):
    """
    Generates and returns a PNG image chart of employees grouped by department.
    """
    plot_buffer = analysis_utils.plot_empleados_por_departamento(db)
    if not isinstance(plot_buffer, io.BytesIO): # pragma: no cover
        if isinstance(plot_buffer, bytes):
            plot_buffer = io.BytesIO(plot_buffer)
        else:
            raise ValueError("Plot generation returned an unexpected buffer type.")

    return StreamingResponse(plot_buffer, media_type="image/png")

@router.get("/charts/licencias_por_software", response_class=StreamingResponse)
async def get_licencias_por_software_chart(db: Session = Depends(get_db)):
    """
    Generates and returns a PNG image chart of licenses grouped by software name.
    """
    plot_buffer = analysis_utils.plot_licencias_por_software(db)
    if not isinstance(plot_buffer, io.BytesIO): # pragma: no cover
        if isinstance(plot_buffer, bytes):
            plot_buffer = io.BytesIO(plot_buffer)
        else:
            raise ValueError("Plot generation returned an unexpected buffer type.")

    return StreamingResponse(plot_buffer, media_type="image/png")

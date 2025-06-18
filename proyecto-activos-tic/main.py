from fastapi import FastAPI
from app.database import create_db_and_tables

# Import models here to ensure they are registered with Base before table creation
from app.auth import models as auth_models # Existing auth models
from app.models import employee_models # Employee SQLAlchemy model
from app.models import hardware_models # Hardware SQLAlchemy model
from app.models import license_models # License SQLAlchemy model
from app.models import web_access_models # Web Access SQLAlchemy model
# from app.models import asset_assignment_models # Future assignment models


# Call this function to create tables when the application starts
# This needs Base from app.database to have all models registered.
# The imports above should handle this as models use app.database.Base
create_db_and_tables()

app = FastAPI(title="Sistema de Gestión de Activos TIC", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Bienvenido al Sistema de Gestión de Activos TIC"}

# Further imports and routes will be added later
from app.auth import routes as auth_routes
from app.routes import employee_routes # Employee routes
from app.routes import hardware_routes # Hardware routes
from app.routes import license_routes # License routes
from app.routes import web_access_routes # Web Access routes
from app.routes import export_routes # Export routes
# from app.routes import asset_assignment_routes # Future Assignment routes

app.include_router(auth_routes.router)
app.include_router(employee_routes.router)
app.include_router(hardware_routes.router)
app.include_router(license_routes.router)
app.include_router(web_access_routes.router)
app.include_router(export_routes.router)
# app.include_router(asset_assignment_routes.router)

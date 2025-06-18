from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse # Added FileResponse & HTMLResponse

from app.database import create_db_and_tables
import os # For checking file existence

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

# Mount static files directories
# IMPORTANT: Ensure these directories exist at the root of your project where main.py is run,
# or adjust paths accordingly. The current setup assumes 'frontend/' and 'static/' are at the same level as 'main.py'
# or that main.py is run from the project root 'proyecto-activos-tic'.
# Given the project structure, these paths should be relative to 'proyecto-activos-tic'
# So, if running from within 'proyecto-activos-tic', paths are "frontend/css", "frontend/js", "static"
# The StaticFiles(directory=...) path is relative to where the Python script is run.
# If main.py is in 'proyecto-activos-tic/app', then paths might need to be "../frontend/css" etc.
# Assuming main.py is at 'proyecto-activos-tic/main.py' (top level of the project)

# Ensure static directories exist to prevent errors on startup if they are missing
os.makedirs("frontend/css", exist_ok=True)
os.makedirs("frontend/js", exist_ok=True)
os.makedirs("frontend/pages", exist_ok=True) # Ensure pages dir exists
os.makedirs("static", exist_ok=True) # For general images like logos, etc.

app.mount("/static/css", StaticFiles(directory="frontend/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="frontend/js"), name="static_js")
app.mount("/static/img", StaticFiles(directory="static"), name="static_img")


@app.get("/", response_class=HTMLResponse)
async def read_login_page():
    login_page_path = "frontend/pages/login.html"
    if not os.path.exists(login_page_path):
        raise HTTPException(status_code=404, detail="Login page not found. Please create frontend/pages/login.html")
    try:
        with open(login_page_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError: # Should be caught by os.path.exists, but as a fallback
        raise HTTPException(status_code=404, detail="Login page not found at path.")


@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard_page():
    dashboard_page_path = "frontend/pages/dashboard.html"
    if not os.path.exists(dashboard_page_path):
        raise HTTPException(status_code=404, detail="Dashboard page not found. Please create frontend/pages/dashboard.html")
    try:
        # Note: Actual dashboard access should be protected by checking auth token here
        # or relying on API calls within dashboard.js to fail if not authenticated.
        # This route just serves the HTML.
        with open(dashboard_page_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard page not found at path.")


@app.get("/acta.html", response_class=HTMLResponse)
async def read_acta_page():
    acta_page_path = "frontend/pages/acta.html"
    if not os.path.exists(acta_page_path):
        raise HTTPException(status_code=404, detail="Acta page not found. Please create frontend/pages/acta.html")
    try:
        with open(acta_page_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError: # Fallback
        raise HTTPException(status_code=404, detail="Acta page not found at path.")

# API Routers
from app.auth import routes as auth_routes
from app.routes import employee_routes # Employee routes
from app.routes import hardware_routes # Hardware routes
from app.routes import license_routes # License routes
from app.routes import web_access_routes # Web Access routes
from app.routes import export_routes # Export routes
from app.routes import analysis_routes # Clean re-import for analysis_routes
# from app.routes import asset_assignment_routes # Future Assignment routes

app.include_router(auth_routes.router)
app.include_router(employee_routes.router)
app.include_router(hardware_routes.router)
app.include_router(license_routes.router)
app.include_router(web_access_routes.router)
app.include_router(export_routes.router)
app.include_router(analysis_routes.router) # Clean re-inclusion for analysis_routes
# app.include_router(asset_assignment_routes.router)

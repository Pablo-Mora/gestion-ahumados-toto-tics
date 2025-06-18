import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session

# CRUD functions
from app.crud import hardware_crud, employee_crud, license_crud
# Potentially others like employee_crud, license_crud if more plots are added

# Pydantic Schemas (optional, if transformation before DataFrame is complex)
# from app.models import hardware_schemas, employee_schemas, license_schemas

# Configure Matplotlib to use a non-interactive backend (Agg)
# This is important for running in a headless environment like a server.
import matplotlib
matplotlib.use('Agg')


def plot_activos_por_tipo(db: Session) -> BytesIO:
    # Placeholder for implementation
    hardware_list_db = hardware_crud.get_hardware_items(db, limit=-1)
    if not hardware_list_db:
        # Create a plot indicating "No data"
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, "No hay datos de hardware para mostrar.",
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=16, color='gray')
        plt.title('Activos por Tipo')
        plt.xlabel('Tipo de Activo')
        plt.ylabel('Cantidad')
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
    else:
        df = pd.DataFrame([h.__dict__ for h in hardware_list_db])
        # Ensure 'tipo_equipo' is the correct column name based on your model
        data_counts = df['tipo_equipo'].value_counts()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=data_counts.index, y=data_counts.values)
        plt.title('Activos por Tipo')
        plt.xlabel('Tipo de Activo')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45, ha="right") # ha="right" for better alignment
        plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close() # Close the plot to free memory
    buf.seek(0)
    return buf


def plot_licencias_por_software(db: Session) -> BytesIO:
    licenses_db = license_crud.get_licenses(db, limit=-1)

    if not licenses_db:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, "No hay datos de licencias para mostrar.",
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=16, color='gray')
        plt.title('Licencias por Software')
        plt.xlabel('Software')
        plt.ylabel('Cantidad de Licencias')
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
    else:
        # Convert list of ORM objects to list of dictionaries
        licenses_data = [lic.__dict__ for lic in licenses_db]
        df = pd.DataFrame(licenses_data)

        data_counts = df['software_nombre'].value_counts()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=data_counts.index, y=data_counts.values)
        plt.title('Licencias por Software')
        plt.xlabel('Software')
        plt.ylabel('Cantidad de Licencias')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf


def plot_empleados_por_departamento(db: Session) -> BytesIO:
    employees_db = employee_crud.get_employees(db, limit=-1)

    if not employees_db:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, "No hay datos de empleados para mostrar.",
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=16, color='gray')
        plt.title('Empleados por Departamento')
        plt.xlabel('Departamento')
        plt.ylabel('Cantidad de Empleados')
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
    else:
        # Convert list of ORM objects to list of dictionaries
        employees_data = [emp.__dict__ for emp in employees_db]
        df = pd.DataFrame(employees_data)

        # Handle missing 'departamento' values by filling with 'No asignado'
        df['departamento'] = df['departamento'].fillna('No asignado')

        data_counts = df['departamento'].value_counts()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=data_counts.index, y=data_counts.values)
        plt.title('Empleados por Departamento')
        plt.xlabel('Departamento')
        plt.ylabel('Cantidad de Empleados')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

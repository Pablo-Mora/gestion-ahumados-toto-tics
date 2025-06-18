# Sistema de Gestión de Activos TIC

## Descripción Breve

Este proyecto es un sistema de gestión de activos de Tecnologías de la Información y Comunicación (TIC) diseñado para ayudar a las organizaciones a rastrear y administrar eficientemente su inventario de hardware, software (licencias) y accesos web asignados a los empleados. La aplicación cuenta con una API backend desarrollada con FastAPI y una interfaz frontend básica para la interacción del usuario.

## Tecnologías Utilizadas

*   **Backend:**
    *   Python 3.10+
    *   FastAPI: Framework web moderno y rápido para construir APIs.
    *   SQLAlchemy: ORM para la interacción con la base de datos.
    *   Pydantic: Para validación de datos y configuración de esquemas.
    *   Uvicorn: Servidor ASGI para FastAPI.
    *   Passlib & python-jose: Para hashing de contraseñas y manejo de JWT (autenticación).
    *   Pandas & Openpyxl: Para la generación de reportes en Excel.
    *   python-docx: Para la generación de documentos Word (Actas de Entrega).
    *   Matplotlib & Seaborn: Para la generación de gráficos de análisis.
*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (Vanilla JS)
    *   html2pdf.js (para la descarga de actas en PDF)
*   **Base de Datos:**
    *   SQLite (por defecto para desarrollo, configurable para otras bases de datos SQL).

## Estructura del Proyecto

El proyecto sigue una estructura modular para separar las preocupaciones:

```
proyecto-activos-tic/
├── app/                     # Lógica principal de la aplicación backend
│   ├── __init__.py
│   ├── analysis/            # Módulos de análisis y generación de gráficos
│   │   ├── __init__.py
│   │   └── analysis_utils.py
│   ├── auth/                # Autenticación (JWT, hashing, modelos de usuario, rutas)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── crud/                # Operaciones CRUD para cada entidad
│   │   ├── __init__.py
│   │   ├── employee_crud.py
│   │   ├── hardware_crud.py
│   │   ├── license_crud.py
│   │   └── web_access_crud.py
│   ├── database.py          # Configuración de la base de datos (engine, SessionLocal, Base)
│   ├── models/              # Modelos SQLAlchemy y esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── employee_models.py
│   │   ├── employee_schemas.py
│   │   ├── hardware_models.py
│   │   ├── hardware_schemas.py
│   │   ├── license_models.py
│   │   ├── license_schemas.py
│   │   ├── web_access_models.py
│   │   └── web_access_schemas.py
│   ├── routes/              # Rutas API para cada entidad
│   │   ├── __init__.py
│   │   ├── analysis_routes.py
│   │   ├── employee_routes.py
│   │   ├── export_routes.py
│   │   ├── hardware_routes.py
│   │   ├── license_routes.py
│   │   └── web_access_routes.py
│   └── utils/               # Utilidades (ej. exportación de datos)
│       ├── __init__.py
│       └── export_utils.py
├── frontend/                # Archivos del frontend
│   ├── css/
│   │   ├── acta_styles.css
│   │   └── styles.css
│   ├── js/
│   │   ├── acta.js
│   │   ├── auth.js
│   │   └── dashboard.js
│   └── pages/
│       ├── acta.html
│       ├── dashboard.html
│       └── login.html
├── static/                  # Archivos estáticos generales (ej. imágenes, logos)
│   └── (vacío por ahora)
├── exports/                 # Directorio para reportes generados (Excel, Word)
│   └── (se crea automáticamente)
├── main.py                  # Archivo principal de FastAPI para iniciar la aplicación
├── requirements.txt         # Dependencias del proyecto Python
└── README.md                # Este archivo
```

## Características Principales

*   Autenticación de usuarios basada en JWT (tokens).
*   Roles de usuario (ADMIN, USER) con acceso diferenciado (registro de usuarios solo para ADMIN).
*   Gestión CRUD completa para:
    *   Empleados
    *   Hardware
    *   Licencias de Software
    *   Accesos Web (credenciales)
*   Generación de reportes:
    *   Reporte general de activos en formato Excel.
    *   "Acta de Entrega" de activos por empleado en formato Word (generada vía HTML y descargable como PDF).
*   Análisis de datos con visualizaciones:
    *   Gráfico de activos por tipo.
    *   Gráfico de empleados por departamento.
    *   Gráfico de licencias por software.
*   Interfaz de usuario web básica para login y dashboard interactivo.
*   Dashboard con sidebar de navegación, carga dinámica de contenido y modales para operaciones CRUD.
*   Funcionalidad de búsqueda en tablas (ej. empleados).
*   Diseño responsive básico para el dashboard.

## Configuración e Instalación

Siga estos pasos para poner en funcionamiento el proyecto localmente:

### Prerrequisitos

*   Python 3.8 o superior.
*   `pip` (manejador de paquetes de Python).
*   Opcional: `git` para clonar el repositorio.

### Pasos

1.  **Clonar el repositorio (si aplica):**
    ```bash
    git clone <url_del_repositorio>
    cd proyecto-activos-tic
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    Activar el entorno virtual:
    *   En Windows: `venv\Scripts\activate`
    *   En macOS/Linux: `source venv/bin/activate`

3.  **Instalar dependencias:**
    Asegúrese de que el archivo `requirements.txt` esté en la raíz del proyecto.
    ```bash
    pip install -r requirements.txt
    ```

    **Nota sobre variables de entorno (Opcional para desarrollo local):**
    Para configurar variables como `SECRET_KEY` localmente, puede crear un archivo `.env` en la raíz del proyecto (`proyecto-activos-tic/.env`). La aplicación intentará cargar estas variables al inicio.
    Ejemplo de contenido para `.env`:
    ```env
    SECRET_KEY="su_clave_secreta_fuerte_y_aleatoria_aqui"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    # SQLALCHEMY_DATABASE_URL="postgresql://user:pass@host:port/dbname" # Ejemplo para DB externa
    ```
    **Importante:** No incluya el archivo `.env` en su control de versiones (git) si contiene información sensible. Añada `.env` a su archivo `.gitignore`. Para producción, las variables de entorno deben configurarse directamente en el servidor o plataforma de despliegue.

4.  **Ejecutar la aplicación:**
    Desde la raíz del proyecto (`proyecto-activos-tic`), donde se encuentra `main.py`:
    ```bash
    uvicorn main:app --reload
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000`.

## API Endpoints

La documentación interactiva de la API (Swagger UI) está disponible en la ruta `/docs` (ej. `http://127.0.0.1:8000/docs`) cuando la aplicación está en ejecución. Desde allí se pueden probar todos los endpoints.

Alternativamente, la documentación ReDoc se encuentra en `/redoc`.

## Creación del Primer Usuario Administrador

El sistema requiere que al menos un usuario administrador exista para poder registrar nuevos usuarios a través de la interfaz. Dado que la ruta de creación de usuarios está protegida y requiere autenticación de administrador:

1.  **Opción 1: Script (Recomendado para inicio limpio)**
    *   Puede crear un script Python simple en la raíz del proyecto (ej. `create_admin.py`) para insertar el primer administrador directamente en la base de datos. Este script necesitaría importar modelos, la función de hash de contraseñas y la configuración de la base de datos.
    *   *Un ejemplo conceptual del script se encuentra comentado en `app/auth/routes.py`.* Ejecútelo una vez con `python create_admin.py` después de que la base de datos (`tic_assets.db`) haya sido creada por la primera ejecución de FastAPI.

2.  **Opción 2: Modificación Temporal del Código (Menos recomendado)**
    *   Temporalmente, podría remover la dependencia `Depends(auth.get_current_admin_user)` de la ruta `create_new_user` en `app/auth/routes.py`.
    *   Ejecutar la aplicación, registrar el primer usuario con rol "ADMIN" usando un cliente API como Postman o Insomnia (o si la UI lo permitiera sin login, que no es el caso actual).
    *   **Importante:** Volver a proteger la ruta inmediatamente después.

Una vez creado el administrador, puede iniciar sesión en la interfaz web y registrar otros usuarios.

## Notas de Despliegue

*   **Base de Datos:** Para producción, considere usar una base de datos más robusta como PostgreSQL o MySQL en lugar de SQLite. Modifique `SQLALCHEMY_DATABASE_URL` en `app/database.py` accordingly.
*   **Entorno Virtual:** Siempre use entornos virtuales para aislar las dependencias del proyecto.
*   **Variables de Entorno:** Para configuraciones sensibles como `SECRET_KEY` de JWT o credenciales de base de datos, use variables de entorno en lugar de valores hardcodeados. Pydantic ofrece soporte para esto.
*   **Servidor ASGI:** Uvicorn es adecuado para desarrollo. Para producción, puede usar Uvicorn con Gunicorn como manejador de procesos para mayor robustez y escalabilidad.
*   **HTTPS:** Asegúrese de que la aplicación se sirva sobre HTTPS en producción. Un proxy inverso como Nginx o Caddy puede manejar esto.
*   **Archivos Estáticos:** En producción, puede ser más eficiente servir archivos estáticos directamente desde un servidor web como Nginx o usar un CDN.
*   **CORS:** Configure `CORSMiddleware` en `main.py` si su frontend y backend se sirven desde dominios diferentes.
*   **Procfile:** Se incluye un archivo `Procfile` para plataformas como Heroku:
    ```
    web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}
    ```
    Esto permite a la plataforma de despliegue saber cómo iniciar la aplicación web. La variable `PORT` es usualmente provista por la plataforma.

Este README provee una guía básica. Ajustes específicos pueden ser necesarios dependiendo del entorno de despliegue.

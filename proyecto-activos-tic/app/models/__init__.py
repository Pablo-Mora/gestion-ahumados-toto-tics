# This file makes app/models a Python package.

# Import models and schemas for easier access, e.g.:
# from app.models import Employee, EmployeeCreate

# Will be populated as models and schemas are defined.

# Import SQLAlchemy models
from .employee_models import Employee
from .hardware_models import Hardware
from .license_models import License
from .web_access_models import WebAccess
# from .asset_assignment_models import AssetAssignment # Example for future

# Import Pydantic schemas
# Employee schemas
from .employee_schemas import EmployeeBase as EmployeeBaseSchema
from .employee_schemas import EmployeeCreate as EmployeeCreateSchema
from .employee_schemas import EmployeeUpdate as EmployeeUpdateSchema
from .employee_schemas import Employee as EmployeeSchema

# Hardware schemas
from .hardware_schemas import HardwareBase as HardwareBaseSchema
from .hardware_schemas import HardwareCreate as HardwareCreateSchema
from .hardware_schemas import HardwareUpdate as HardwareUpdateSchema
from .hardware_schemas import Hardware as HardwareSchema

# License schemas
from .license_schemas import LicenseBase as LicenseBaseSchema
from .license_schemas import LicenseCreate as LicenseCreateSchema
from .license_schemas import LicenseUpdate as LicenseUpdateSchema
from .license_schemas import License as LicenseSchema

# Web Access schemas
from .web_access_schemas import WebAccessBase as WebAccessBaseSchema
from .web_access_schemas import WebAccessCreate as WebAccessCreateSchema
from .web_access_schemas import WebAccessUpdate as WebAccessUpdateSchema
from .web_access_schemas import WebAccess as WebAccessSchema

# from .asset_assignment_schemas import AssetAssignment as AssetAssignmentSchema

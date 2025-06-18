// Store current user info globally or in a dedicated object
let currentUser = null;
const API_BASE_URL = ''; // Assuming FastAPI runs on the same domain/port

// Modal elements (Employee)
const employeeModal = document.getElementById('employeeModal');
const employeeForm = document.getElementById('employeeForm');
const employeeModalTitle = document.getElementById('employeeModalTitle');
const employeeFormError = document.getElementById('employeeFormError');
const closeEmployeeModalBtn = document.getElementById('closeEmployeeModal');
const employeeIdField = document.getElementById('employeeId');

// Modal elements (Hardware) - Initialize these
const hardwareModal = document.getElementById('hardwareModal');
const hardwareForm = document.getElementById('hardwareForm');
const hardwareModalTitle = document.getElementById('hardwareModalTitle');
const hardwareFormError = document.getElementById('hardwareFormError');
const closeHardwareModalBtn = document.getElementById('closeHardwareModal');
const hardwareIdField = document.getElementById('hardwareId');

// Modal elements (License) - Initialize these
const licenseModal = document.getElementById('licenseModal');
const licenseForm = document.getElementById('licenseForm');
const licenseModalTitle = document.getElementById('licenseModalTitle');
const licenseFormError = document.getElementById('licenseFormError');
const closeLicenseModalBtn = document.getElementById('closeLicenseModal');
const licenseIdField = document.getElementById('licenseId');

// Modal elements (Web Access) - Initialize these
const webAccessModal = document.getElementById('webAccessModal');
const webAccessForm = document.getElementById('webAccessForm');
const webAccessModalTitle = document.getElementById('webAccessModalTitle');
const webAccessFormError = document.getElementById('webAccessFormError');
const closeWebAccessModalBtn = document.getElementById('closeWebAccessModal');
const webAccessIdField = document.getElementById('webAccessId');
const passwordWebAccessGroup = document.getElementById('passwordWebAccessGroup');

// Modal elements (User Registration) - Initialize these
const userRegistrationModal = document.getElementById('userRegistrationModal');
const userRegistrationForm = document.getElementById('userRegistrationForm');
const userRegModalTitle = document.getElementById('userRegModalTitle'); // Though title is static here
const userRegFormError = document.getElementById('userRegFormError');
const closeUserRegModalBtn = document.getElementById('closeUserRegModal');

// Global message element
const globalMessageDiv = document.getElementById('globalMessage');

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        window.location.href = '/'; // Redirect to login if no token
        return;
    }

    await fetchCurrentUserInfo();
    setupNavigation();

    const dashboardHomeLink = document.getElementById('navDashboardHome');
    if (dashboardHomeLink) {
        loadDashboardHome();
        setActiveLink(dashboardHomeLink);
    }

    // Setup Modal close buttons
    if (closeEmployeeModalBtn) {
        closeEmployeeModalBtn.onclick = () => { if(employeeModal) employeeModal.style.display = 'none'; };
    }
    if (closeHardwareModalBtn) {
        closeHardwareModalBtn.onclick = () => { if(hardwareModal) hardwareModal.style.display = 'none'; };
    }
    if (closeLicenseModalBtn) {
        closeLicenseModalBtn.onclick = () => { if(licenseModal) licenseModal.style.display = 'none'; };
    }
    if (closeWebAccessModalBtn) {
        closeWebAccessModalBtn.onclick = () => { if(webAccessModal) webAccessModal.style.display = 'none'; };
    }
    if (closeUserRegModalBtn) { // Add listener for user registration modal
        closeUserRegModalBtn.onclick = () => { if(userRegistrationModal) userRegistrationModal.style.display = 'none'; };
    }

    // Close modal if clicked outside content
    window.onclick = function(event) {
        if (event.target == employeeModal && employeeModal) {
            employeeModal.style.display = 'none';
        }
        if (event.target == hardwareModal && hardwareModal) {
            hardwareModal.style.display = 'none';
        }
        if (event.target == licenseModal && licenseModal) {
            licenseModal.style.display = 'none';
        }
        if (event.target == webAccessModal && webAccessModal) {
            webAccessModal.style.display = 'none';
        }
        if (event.target == userRegistrationModal && userRegistrationModal) { // Add for user reg modal
            userRegistrationModal.style.display = 'none';
        }
    }

    // Form Submit Listeners
    if (employeeForm) {
        employeeForm.addEventListener('submit', handleEmployeeFormSubmit);
    }
    if (hardwareForm) {
        hardwareForm.addEventListener('submit', handleHardwareFormSubmit);
    }
    if (licenseForm) {
        licenseForm.addEventListener('submit', handleLicenseFormSubmit);
    }
    if (webAccessForm) {
        webAccessForm.addEventListener('submit', handleWebAccessFormSubmit);
    }
    if (userRegistrationForm) {
        userRegistrationForm.addEventListener('submit', handleUserRegistrationFormSubmit);
    }

    // Sidebar Toggle Logic
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('.sidebar');
    // const dashboardContainer = document.querySelector('.dashboard-container'); // Not strictly needed if not pushing content

    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            // if (dashboardContainer) dashboardContainer.classList.toggle('sidebar-open');
        });

        // Close sidebar when clicking on a nav link on mobile
        document.querySelectorAll('.sidebar-nav li a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
                    sidebar.classList.remove('open');
                    // if (dashboardContainer) dashboardContainer.classList.remove('sidebar-open');
                }
            });
        });

        // Optional: Close sidebar if clicking outside of it on mobile (on main-content)
        const mainContentArea = document.querySelector('.main-content');
        if (mainContentArea) {
            mainContentArea.addEventListener('click', function(event) {
              if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
                  // Ensure the click is not on the toggle button itself, which has its own handler
                  if (sidebarToggleBtn && !sidebarToggleBtn.contains(event.target)) {
                    sidebar.classList.remove('open');
                    // if (dashboardContainer) dashboardContainer.classList.remove('sidebar-open');
                  }
              }
            });
        }
    }
});

async function fetchCurrentUserInfo() {
    const token = localStorage.getItem('accessToken');
    if (!token) { logout(); return; }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/users/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            currentUser = await response.json();
            const userInfoP = document.getElementById('userInfo');
            if (userInfoP) userInfoP.textContent = `Usuario: ${currentUser.username} (${currentUser.role})`;

            const adminOnlyNav = document.getElementById('adminOnlyNav');
            if (adminOnlyNav) { // Ensure element exists before trying to style it
                if (currentUser.role === 'ADMIN') {
                    adminOnlyNav.style.display = 'block';
                } else {
                    adminOnlyNav.style.display = 'none';
                }
            }
        } else if (response.status === 401) {
            console.warn("User info fetch unauthorized. Logging out.");
            logout();
        } else {
            console.error('Error fetching user info:', response.statusText);
            const userInfoP = document.getElementById('userInfo');
            if (userInfoP) userInfoP.textContent = 'Error cargando usuario.';
        }
    } catch (error) {
        console.error('Failed to fetch user info:', error);
        const userInfoP = document.getElementById('userInfo');
        if (userInfoP) userInfoP.textContent = 'Error de conexión.';
    }
}

function setupNavigation() {
    document.getElementById('navDashboardHome').addEventListener('click', (e) => { e.preventDefault(); loadDashboardHome(); setActiveLink(e.target); });
    document.getElementById('navEmpleados').addEventListener('click', (e) => { e.preventDefault(); loadEmpleados(); setActiveLink(e.target); });
    document.getElementById('navHardware').addEventListener('click', (e) => { e.preventDefault(); loadHardware(); setActiveLink(e.target); });
    document.getElementById('navLicencias').addEventListener('click', (e) => { e.preventDefault(); loadLicencias(); setActiveLink(e.target); });
    document.getElementById('navAccesos').addEventListener('click', (e) => { e.preventDefault(); loadAccesos(); setActiveLink(e.target); });
    document.getElementById('navReportes').addEventListener('click', (e) => { e.preventDefault(); loadReportes(); setActiveLink(e.target); });
    document.getElementById('navAnalisis').addEventListener('click', (e) => { e.preventDefault(); loadAnalisis(); setActiveLink(e.target); });

    if (currentUser && currentUser.role === 'ADMIN') {
        const navRegistrarUsuario = document.getElementById('navRegistrarUsuario');
        if (navRegistrarUsuario) {
             navRegistrarUsuario.addEventListener('click', (e) => { e.preventDefault(); loadUserRegistrationForm(); setActiveLink(e.target); });
        }
    }
}

function setActiveLink(activeLink) {
    document.querySelectorAll('.sidebar-nav li a').forEach(link => link.classList.remove('active'));
    if (activeLink) activeLink.classList.add('active');
}

function updateMainHeader(title) {
    document.querySelector('.main-header h1').textContent = title;
}

function showGlobalMessage(message, type = 'success') {
    if (!globalMessageDiv) return; // Safety check
    globalMessageDiv.textContent = message;
    globalMessageDiv.className = 'global-message ' + type; // Reset classes then add type
    globalMessageDiv.style.display = 'block';
    setTimeout(() => { globalMessageDiv.style.display = 'none'; }, 3000);
}

function getFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};
    formData.forEach((value, key) => { data[key] = value; });
    return data;
}

async function openEmployeeModal(employeeIdToEdit = null) {
    if (!employeeModal || !employeeForm || !employeeModalTitle || !employeeIdField || !employeeFormError) {
        console.error("Modal elements not found."); return;
    }
    employeeForm.reset();
    employeeIdField.value = '';
    employeeFormError.style.display = 'none';
    employeeFormError.textContent = '';

    if (employeeIdToEdit) {
        employeeModalTitle.textContent = 'Editar Empleado';
        employeeIdField.value = employeeIdToEdit;
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/employees/\${employeeIdToEdit}\`, {
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (!response.ok) {
                if (response.status === 401) logout();
                throw new Error('Failed to fetch employee details.');
            }
            const emp = await response.json();
            document.getElementById('nombre').value = emp.nombre;
            document.getElementById('identificacion').value = emp.identificacion;
            document.getElementById('cargo').value = emp.cargo;
            document.getElementById('departamento').value = emp.departamento || '';
        } catch (error) {
            console.error(error);
            employeeFormError.textContent = 'Error al cargar datos del empleado.';
            employeeFormError.style.display = 'block';
            return;
        }
    } else {
        employeeModalTitle.textContent = 'Agregar Empleado';
    }
    employeeModal.style.display = 'block';
}

async function handleEmployeeFormSubmit(event) {
    event.preventDefault();
    if (!employeeFormError) return; // Safety check
    employeeFormError.style.display = 'none';
    employeeFormError.textContent = '';

    // Client-side validation example
    const nombre = document.getElementById('nombre').value;
    const identificacion = document.getElementById('identificacion').value;
    const cargo = document.getElementById('cargo').value;

    if (!nombre.trim() || !identificacion.trim() || !cargo.trim()) {
        employeeFormError.textContent = 'Nombre, Identificación y Cargo son obligatorios.';
        employeeFormError.style.display = 'block';
        return; // Stop submission
    }
    // Add more specific validations if needed, e.g., format of 'identificacion'

    const employeeId = employeeIdField.value;
    const method = employeeId ? 'PUT' : 'POST';
    const url = employeeId ? \`\${API_BASE_URL}/employees/\${employeeId}\` : \`\${API_BASE_URL}/employees/\`;
    const token = localStorage.getItem('accessToken');

    const formData = getFormData(employeeForm);
    const body = {
        nombre: formData.nombre,
        identificacion: formData.identificacion,
        cargo: formData.cargo,
        departamento: formData.departamento || null
    };

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': \`Bearer \${token}\`
            },
            body: JSON.stringify(body)
        });
        if (response.ok) {
            if (employeeModal) employeeModal.style.display = 'none';
            loadEmpleados();
            showGlobalMessage(\`Empleado \${employeeId ? 'actualizado' : 'agregado'} con éxito.\`);
        } else {
            if (response.status === 401) logout();
            const errorData = await response.json();
            employeeFormError.textContent = errorData.detail || \`Error al guardar empleado (\${response.status})\`;
            employeeFormError.style.display = 'block';
        }
    } catch (error) {
        console.error('Error saving employee:', error);
        employeeFormError.textContent = 'Ocurrió un error de red.';
        employeeFormError.style.display = 'block';
    }
}

function loadDashboardHome() {
    updateMainHeader('Dashboard General');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = \`
        <h2>Estadísticas Rápidas</h2>
        <p>Aquí se mostrarán algunas estadísticas generales del sistema.</p>
        <h3>Activos por Tipo</h3>
        <img src="/analysis/charts/activos_por_tipo?_=\${new Date().getTime()}" alt="Gráfico de Activos por Tipo">
    \`;
}

async function loadEmpleados() {
    updateMainHeader('Gestión de Empleados');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = '<p>Cargando empleados...</p>';
    const token = localStorage.getItem('accessToken');

    try {
        const response = await fetch(\`\${API_BASE_URL}/employees/\`, {
            headers: { 'Authorization': \`Bearer \${token}\` }
        });
        if (!response.ok) {
            if (response.status === 401) logout();
            throw new Error(\`Error fetching employees: (\${response.status}) \${response.statusText}\`);
        }

        const empleados = await response.json();
        let tableHtml = '<div class="table-controls"><input type="text" id="searchEmployeeInput" placeholder="Buscar empleado..." style="margin-bottom:10px;"></div>';
        tableHtml += '<h2>Lista de Empleados</h2><button id="addEmployeeBtn" class="btn-add" style="margin-bottom:15px; padding: 8px 15px; background-color: #28a745;">Agregar Empleado</button>';
        tableHtml += '<table class="data-table"><thead><tr><th>ID</th><th>Nombre</th><th>Identificación</th><th>Cargo</th><th>Departamento</th><th>Acciones</th></tr></thead><tbody>';

        empleados.forEach(emp => {
            tableHtml += \`
                <tr>
                    <td>\${emp.id}</td>
                    <td>\${emp.nombre}</td>
                    <td>\${emp.identificacion}</td>
                    <td>\${emp.cargo}</td>
                    <td>\${emp.departamento || 'N/A'}</td>
                    <td class="table-actions">
                        <button class="btn-edit" onclick="editEmployee(\${emp.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteEmployee(\${emp.id})">Eliminar</button>
                    </td>
                </tr>
            \`;
        });
        tableHtml += '</tbody></table>';
        contentArea.innerHTML = tableHtml;

        const addEmployeeBtn = document.getElementById('addEmployeeBtn');
        if (addEmployeeBtn) {
            addEmployeeBtn.addEventListener('click', () => openEmployeeModal());
        }

        const searchInput = document.getElementById('searchEmployeeInput');
        if (searchInput) {
            searchInput.addEventListener('keyup', () => {
                const filter = searchInput.value.toLowerCase();
                const table = contentArea.querySelector('.data-table');
                if (!table) return;
                const rows = table.getElementsByTagName('tr');
                for (let i = 1; i < rows.length; i++) { // Start from 1 to skip header row (index 0)
                    let visible = false;
                    const cells = rows[i].getElementsByTagName('td');
                    // Iterate through relevant cells for searching (e.g., skip actions cell)
                    for (let j = 0; j < cells.length - 1; j++) {
                        if (cells[j]) {
                            if (cells[j].textContent.toLowerCase().includes(filter)) {
                                visible = true;
                                break;
                            }
                        }
                    }
                    rows[i].style.display = visible ? '' : 'none';
                }
            });
        }
    } catch (error) {
        console.error(error);
        contentArea.innerHTML = \`<p>\${error.message || 'Error al cargar empleados.'}</p>\`;
    }
}

function editEmployee(id) { // This function is now a wrapper to call openEmployeeModal
    openEmployeeModal(id);
}

async function deleteEmployee(id) {
    if(confirm(\`¿Está seguro de eliminar empleado ID: \${id}?\`)) {
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/employees/\${id}\`, {
                method: 'DELETE',
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (response.ok) {
                showGlobalMessage('Empleado eliminado con éxito.');
                loadEmpleados(); // Refresh table
            } else {
                if (response.status === 401) logout();
                const errorData = await response.json();
                showGlobalMessage(errorData.detail || 'Error al eliminar empleado.', 'error');
            }
        } catch (error) {
            console.error('Error deleting employee:', error);
            showGlobalMessage('Ocurrió un error de red al eliminar.', 'error');
        }
    }
}

// Functions for Hardware CRUD
async function loadHardware() {
    updateMainHeader('Gestión de Hardware');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = '<p>Cargando hardware...</p>';
    const token = localStorage.getItem('accessToken');

    try {
        const response = await fetch(\`\${API_BASE_URL}/hardware/\`, {
            headers: { 'Authorization': \`Bearer \${token}\` }
        });
        if (!response.ok) {
            if (response.status === 401) logout();
            throw new Error(\`Error fetching hardware: (\${response.status}) \${response.statusText}\`);
        }

        const hardwareList = await response.json();
        let tableHtml = '<h2>Lista de Hardware</h2><button id="addHardwareBtn" class="btn-add" style="margin-bottom:15px; padding: 8px 15px; background-color: #28a745;">Agregar Hardware</button>';
        tableHtml += \`
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Tipo</th>
                        <th>Marca</th>
                        <th>Modelo</th>
                        <th>Serial</th>
                        <th>Estado</th>
                        <th>Empleado ID</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
        \`;

        hardwareList.forEach(hw => {
            tableHtml += \`
                <tr>
                    <td>\${hw.id}</td>
                    <td>\${hw.tipo_equipo}</td>
                    <td>\${hw.marca}</td>
                    <td>\${hw.modelo || 'N/A'}</td>
                    <td>\${hw.serial}</td>
                    <td>\${hw.estado || 'N/A'}</td>
                    <td>\${hw.employee_id || 'No asignado'}</td>
                    <td class="table-actions">
                        <button class="btn-edit" onclick="editHardware(\${hw.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteHardware(\${hw.id})">Eliminar</button>
                    </td>
                </tr>
            \`;
        });
        tableHtml += '</tbody></table>';
        contentArea.innerHTML = tableHtml;

        const addHardwareBtn = document.getElementById('addHardwareBtn');
        if (addHardwareBtn) {
            addHardwareBtn.addEventListener('click', () => openHardwareModal());
        }
    } catch (error) {
        console.error(error);
        contentArea.innerHTML = \`<p>\${error.message || 'Error al cargar hardware.'}</p>\`;
    }
}

async function openHardwareModal(hardwareIdToEdit = null) {
    if (!hardwareModal || !hardwareForm || !hardwareModalTitle || !hardwareIdField || !hardwareFormError) {
        console.error("Hardware modal elements not found."); return;
    }
    hardwareForm.reset();
    hardwareIdField.value = '';
    hardwareFormError.style.display = 'none';
    hardwareFormError.textContent = '';

    if (hardwareIdToEdit) {
        hardwareModalTitle.textContent = 'Editar Hardware';
        hardwareIdField.value = hardwareIdToEdit;
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/hardware/\${hardwareIdToEdit}\`, {
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (!response.ok) {
                if (response.status === 401) logout();
                throw new Error('Failed to fetch hardware details.');
            }
            const hw = await response.json();
            document.getElementById('tipo_equipo').value = hw.tipo_equipo;
            document.getElementById('marca').value = hw.marca;
            document.getElementById('modelo').value = hw.modelo || '';
            document.getElementById('serial').value = hw.serial;
            document.getElementById('numero_activo').value = hw.numero_activo || '';
            document.getElementById('estado').value = hw.estado || 'operativo';
            document.getElementById('ubicacion_actual').value = hw.ubicacion_actual || '';
            document.getElementById('employee_id_hw').value = hw.employee_id || '';
        } catch (error) {
            console.error(error);
            hardwareFormError.textContent = 'Error al cargar datos del hardware.';
            hardwareFormError.style.display = 'block';
            return;
        }
    } else {
        hardwareModalTitle.textContent = 'Agregar Hardware';
    }
    hardwareModal.style.display = 'block';
}

async function handleHardwareFormSubmit(event) {
    event.preventDefault();
    if (!hardwareFormError) return;
    hardwareFormError.style.display = 'none';
    hardwareFormError.textContent = '';

    const hardwareId = hardwareIdField.value;
    const method = hardwareId ? 'PUT' : 'POST';
    const url = hardwareId ? \`\${API_BASE_URL}/hardware/\${hardwareId}\` : \`\${API_BASE_URL}/hardware/\`;
    const token = localStorage.getItem('accessToken');

    const formData = getFormData(hardwareForm);
    const body = {
        tipo_equipo: formData.tipo_equipo,
        marca: formData.marca,
        modelo: formData.modelo || null,
        serial: formData.serial,
        numero_activo: formData.numero_activo || null,
        estado: formData.estado,
        ubicacion_actual: formData.ubicacion_actual || null,
        // Ensure employee_id is an integer or null
        employee_id: formData.employee_id ? parseInt(formData.employee_id, 10) : null
    };
    // Remove employee_id from body if it's NaN (e.g. empty string was parsed)
    if (isNaN(body.employee_id)) body.employee_id = null;


    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': \`Bearer \${token}\`
            },
            body: JSON.stringify(body)
        });
        if (response.ok) {
            if (hardwareModal) hardwareModal.style.display = 'none';
            loadHardware();
            showGlobalMessage(\`Hardware \${hardwareId ? 'actualizado' : 'agregado'} con éxito.\`);
        } else {
            if (response.status === 401) logout();
            const errorData = await response.json();
            hardwareFormError.textContent = errorData.detail || \`Error al guardar hardware (\${response.status})\`;
            hardwareFormError.style.display = 'block';
        }
    } catch (error) {
        console.error('Error saving hardware:', error);
        hardwareFormError.textContent = 'Ocurrió un error de red.';
        hardwareFormError.style.display = 'block';
    }
}

function editHardware(id) {
    openHardwareModal(id);
}

async function deleteHardware(id) {
    if(confirm(\`¿Está seguro de eliminar hardware ID: \${id}?\`)) {
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/hardware/\${id}\`, {
                method: 'DELETE',
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (response.ok) {
                showGlobalMessage('Hardware eliminado con éxito.');
                loadHardware(); // Refresh table
            } else {
                if (response.status === 401) logout();
                const errorData = await response.json();
                showGlobalMessage(errorData.detail || 'Error al eliminar hardware.', 'error');
            }
        } catch (error) {
            console.error('Error deleting hardware:', error);
            showGlobalMessage('Ocurrió un error de red al eliminar.', 'error');
        }
    }
}


// Functions for License CRUD
async function loadLicencias() {
    updateMainHeader('Gestión de Licencias');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = '<p>Cargando licencias...</p>';
    const token = localStorage.getItem('accessToken');

    try {
        const response = await fetch(\`\${API_BASE_URL}/licenses/\`, {
            headers: { 'Authorization': \`Bearer \${token}\` }
        });
        if (!response.ok) {
            if (response.status === 401) logout();
            throw new Error(\`Error fetching licenses: (\${response.status}) \${response.statusText}\`);
        }

        const licenseList = await response.json();
        let tableHtml = '<h2>Lista de Licencias</h2><button id="addLicenseBtn" class="btn-add" style="margin-bottom:15px; padding: 8px 15px; background-color: #28a745;">Agregar Licencia</button>';
        tableHtml += \`
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Software</th>
                        <th>Tipo</th>
                        <th>Vencimiento</th>
                        <th>Empleado ID</th>
                        <th>Hardware ID</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
        \`;

        licenseList.forEach(lic => {
            tableHtml += \`
                <tr>
                    <td>\${lic.id}</td>
                    <td>\${lic.software_nombre}</td>
                    <td>\${lic.tipo_licencia}</td>
                    <td>\${lic.fecha_vencimiento || 'N/A'}</td>
                    <td>\${lic.employee_id || 'N/A'}</td>
                    <td>\${lic.hardware_id || 'N/A'}</td>
                    <td class="table-actions">
                        <button class="btn-edit" onclick="editLicense(\${lic.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteLicense(\${lic.id})">Eliminar</button>
                    </td>
                </tr>
            \`;
        });
        tableHtml += '</tbody></table>';
        contentArea.innerHTML = tableHtml;

        const addLicenseBtn = document.getElementById('addLicenseBtn');
        if (addLicenseBtn) {
            addLicenseBtn.addEventListener('click', () => openLicenseModal());
        }
    } catch (error) {
        console.error(error);
        contentArea.innerHTML = \`<p>\${error.message || 'Error al cargar licencias.'}</p>\`;
    }
}

async function openLicenseModal(licenseIdToEdit = null) {
    if (!licenseModal || !licenseForm || !licenseModalTitle || !licenseIdField || !licenseFormError) {
        console.error("License modal elements not found."); return;
    }
    licenseForm.reset();
    licenseIdField.value = '';
    licenseFormError.style.display = 'none';
    licenseFormError.textContent = '';

    if (licenseIdToEdit) {
        licenseModalTitle.textContent = 'Editar Licencia';
        licenseIdField.value = licenseIdToEdit;
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/licenses/\${licenseIdToEdit}\`, {
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (!response.ok) { if (response.status === 401) logout(); throw new Error('Failed to fetch license details.');}
            const lic = await response.json();
            document.getElementById('software_nombre').value = lic.software_nombre;
            document.getElementById('fabricante').value = lic.fabricante || '';
            document.getElementById('clave_producto').value = lic.clave_producto || '';
            document.getElementById('tipo_licencia').value = lic.tipo_licencia;
            document.getElementById('cantidad_usuarios').value = lic.cantidad_usuarios || 1;
            document.getElementById('fecha_compra').value = lic.fecha_compra || '';
            document.getElementById('fecha_vencimiento').value = lic.fecha_vencimiento || '';
            document.getElementById('proveedor').value = lic.proveedor || '';
            document.getElementById('costo').value = lic.costo || '';
            document.getElementById('notas_lic').value = lic.notas || '';
            document.getElementById('employee_id_lic').value = lic.employee_id || '';
            document.getElementById('hardware_id_lic').value = lic.hardware_id || '';
        } catch (error) {
            console.error(error);
            licenseFormError.textContent = 'Error al cargar datos de la licencia.';
            licenseFormError.style.display = 'block';
            return;
        }
    } else {
        licenseModalTitle.textContent = 'Agregar Licencia';
    }
    licenseModal.style.display = 'block';
}

async function handleLicenseFormSubmit(event) {
    event.preventDefault();
    if (!licenseFormError) return;
    licenseFormError.style.display = 'none';
    licenseFormError.textContent = '';

    const licenseId = licenseIdField.value;
    const method = licenseId ? 'PUT' : 'POST';
    const url = licenseId ? \`\${API_BASE_URL}/licenses/\${licenseId}\` : \`\${API_BASE_URL}/licenses/\`;
    const token = localStorage.getItem('accessToken');

    const formData = getFormData(licenseForm);
    const body = {
        software_nombre: formData.software_nombre,
        fabricante: formData.fabricante || null,
        clave_producto: formData.clave_producto || null,
        tipo_licencia: formData.tipo_licencia,
        cantidad_usuarios: formData.cantidad_usuarios ? parseInt(formData.cantidad_usuarios, 10) : 1,
        fecha_compra: formData.fecha_compra || null,
        fecha_vencimiento: formData.fecha_vencimiento || null,
        proveedor: formData.proveedor || null,
        costo: formData.costo ? parseFloat(formData.costo) : null,
        notas: formData.notas || null,
        employee_id: formData.employee_id ? parseInt(formData.employee_id, 10) : null,
        hardware_id: formData.hardware_id ? parseInt(formData.hardware_id, 10) : null
    };
    if (isNaN(body.employee_id)) body.employee_id = null;
    if (isNaN(body.hardware_id)) body.hardware_id = null;
    if (isNaN(body.cantidad_usuarios)) body.cantidad_usuarios = 1;
    if (isNaN(body.costo)) body.costo = null;


    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json', 'Authorization': \`Bearer \${token}\`},
            body: JSON.stringify(body)
        });
        if (response.ok) {
            if (licenseModal) licenseModal.style.display = 'none';
            loadLicencias();
            showGlobalMessage(\`Licencia \${licenseId ? 'actualizada' : 'agregada'} con éxito.\`);
        } else {
            if (response.status === 401) logout();
            const errorData = await response.json();
            licenseFormError.textContent = errorData.detail || \`Error al guardar licencia (\${response.status})\`;
            licenseFormError.style.display = 'block';
        }
    } catch (error) {
        console.error('Error saving license:', error);
        licenseFormError.textContent = 'Ocurrió un error de red.';
        licenseFormError.style.display = 'block';
    }
}

function editLicense(id) {
    openLicenseModal(id);
}

async function deleteLicense(id) {
    if(confirm(\`¿Está seguro de eliminar licencia ID: \${id}?\`)) {
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/licenses/\${id}\`, {
                method: 'DELETE',
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (response.ok) {
                showGlobalMessage('Licencia eliminada con éxito.');
                loadLicencias(); // Refresh table
            } else {
                if (response.status === 401) logout();
                const errorData = await response.json();
                showGlobalMessage(errorData.detail || 'Error al eliminar licencia.', 'error');
            }
        } catch (error) {
            console.error('Error deleting license:', error);
            showGlobalMessage('Ocurrió un error de red al eliminar.', 'error');
        }
    }
}


// Functions for Web Access CRUD
async function loadAccesos() {
    updateMainHeader('Gestión de Accesos Web');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = '<p>Cargando accesos web...</p>';
    const token = localStorage.getItem('accessToken');

    try {
        // Assuming /web-accesses/ fetches all for admin, or user-specific if not admin (backend logic)
        // Or, use a specific endpoint like /web-accesses/by-employee/{current_user.id} for non-admins
        const response = await fetch(\`\${API_BASE_URL}/web-accesses/\`, { // This gets ALL if admin, or should be user-specific
            headers: { 'Authorization': \`Bearer \${token}\` }
        });
        if (!response.ok) {
            if (response.status === 401) logout();
            throw new Error(\`Error fetching web accesses: (\${response.status}) \${response.statusText}\`);
        }

        const accessList = await response.json();
        let tableHtml = '<h2>Lista de Accesos Web</h2><button id="addWebAccessBtn" class="btn-add" style="margin-bottom:15px; padding: 8px 15px; background-color: #28a745;">Agregar Acceso Web</button>';
        tableHtml += \`
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Servicio</th>
                        <th>URL</th>
                        <th>Usuario</th>
                        <th>Empleado ID</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
        \`;

        accessList.forEach(acc => {
            tableHtml += \`
                <tr>
                    <td>\${acc.id}</td>
                    <td>\${acc.nombre_servicio}</td>
                    <td><a href="\${acc.url}" target="_blank" rel="noopener noreferrer">\${acc.url || 'N/A'}</a></td>
                    <td>\${acc.usuario}</td>
                    <td>\${acc.employee_id}</td>
                    <td class="table-actions">
                        <button class="btn-edit" onclick="editWebAccess(\${acc.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteWebAccess(\${acc.id})">Eliminar</button>
                    </td>
                </tr>
            \`;
        });
        tableHtml += '</tbody></table>';
        contentArea.innerHTML = tableHtml;

        const addWebAccessBtn = document.getElementById('addWebAccessBtn');
        if (addWebAccessBtn) {
            addWebAccessBtn.addEventListener('click', () => openWebAccessModal());
        }
    } catch (error) {
        console.error(error);
        contentArea.innerHTML = \`<p>\${error.message || 'Error al cargar accesos web.'}</p>\`;
    }
}

async function openWebAccessModal(accessIdToEdit = null) {
    if (!webAccessModal || !webAccessForm || !webAccessModalTitle || !webAccessIdField || !webAccessFormError || !passwordWebAccessGroup) {
        console.error("Web Access modal elements not found."); return;
    }
    webAccessForm.reset();
    webAccessIdField.value = '';
    webAccessFormError.style.display = 'none';
    webAccessFormError.textContent = '';
    document.getElementById('password_placeholder_wa').required = false; // Default for edit

    if (accessIdToEdit) {
        webAccessModalTitle.textContent = 'Editar Acceso Web';
        webAccessIdField.value = accessIdToEdit;
        if (passwordWebAccessGroup) passwordWebAccessGroup.querySelector('small').style.display = 'block'; // Show "leave blank" message
        document.getElementById('password_placeholder_wa').placeholder = "Dejar en blanco para no cambiar";


        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/web-accesses/\${accessIdToEdit}\`, {
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (!response.ok) { if (response.status === 401) logout(); throw new Error('Failed to fetch web access details.');}
            const acc = await response.json();
            document.getElementById('nombre_servicio_wa').value = acc.nombre_servicio;
            document.getElementById('url_wa').value = acc.url || '';
            document.getElementById('usuario_wa').value = acc.usuario;
            document.getElementById('descripcion_wa').value = acc.descripcion || '';
            document.getElementById('notas_adicionales_wa').value = acc.notas_adicionales || '';
            document.getElementById('employee_id_wa').value = acc.employee_id;
            // DO NOT populate password field
        } catch (error) {
            console.error(error);
            webAccessFormError.textContent = 'Error al cargar datos del acceso web.';
            webAccessFormError.style.display = 'block';
            return;
        }
    } else {
        webAccessModalTitle.textContent = 'Agregar Acceso Web';
        if (passwordWebAccessGroup) passwordWebAccessGroup.querySelector('small').style.display = 'none'; // Hide "leave blank"
        document.getElementById('password_placeholder_wa').placeholder = "";
        document.getElementById('password_placeholder_wa').required = true; // Password required for new access
    }
    webAccessModal.style.display = 'block';
}

async function handleWebAccessFormSubmit(event) {
    event.preventDefault();
    if (!webAccessFormError) return;
    webAccessFormError.style.display = 'none';
    webAccessFormError.textContent = '';

    // Basic client-side validation example
    const nombreServicio = document.getElementById('nombre_servicio_wa').value;
    const usuario = document.getElementById('usuario_wa').value;
    const employeeIdInput = document.getElementById('employee_id_wa').value;
    const passwordInput = document.getElementById('password_placeholder_wa').value;

    if (!nombreServicio.trim() || !usuario.trim() || !employeeIdInput.trim()) {
        webAccessFormError.textContent = 'Nombre del servicio, usuario e ID de empleado son obligatorios.';
        webAccessFormError.style.display = 'block';
        return;
    }

    const webAccessId = webAccessIdField.value;
    if (!webAccessId && !passwordInput.trim()) { // Password required only for new entries
        webAccessFormError.textContent = 'La contraseña es obligatoria para nuevos accesos.';
        webAccessFormError.style.display = 'block';
        return;
    }


    const method = webAccessId ? 'PUT' : 'POST';
    const url = webAccessId ? \`\${API_BASE_URL}/web-accesses/\${webAccessId}\` : \`\${API_BASE_URL}/web-accesses/\`;
    const token = localStorage.getItem('accessToken');

    const formData = getFormData(webAccessForm);
    const body = {
        nombre_servicio: formData.nombre_servicio,
        url: formData.url || null,
        usuario: formData.usuario,
        descripcion: formData.descripcion || null,
        notas_adicionales: formData.notas_adicionales || null,
        employee_id: parseInt(formData.employee_id, 10),
    };

    // Only include password_placeholder if it's provided (for new or to change)
    if (formData.password_placeholder && formData.password_placeholder.trim() !== '') {
        body.password_placeholder = formData.password_placeholder;
    }
     if (isNaN(body.employee_id)) { // Should be caught by required check, but good fallback
        webAccessFormError.textContent = 'ID de Empleado debe ser un número válido.';
        webAccessFormError.style.display = 'block';
        return;
    }


    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json', 'Authorization': \`Bearer \${token}\`},
            body: JSON.stringify(body)
        });
        if (response.ok) {
            if (webAccessModal) webAccessModal.style.display = 'none';
            loadAccesos();
            showGlobalMessage(\`Acceso Web \${webAccessId ? 'actualizado' : 'agregado'} con éxito.\`);
        } else {
            if (response.status === 401) logout();
            const errorData = await response.json();
            webAccessFormError.textContent = errorData.detail || \`Error al guardar acceso web (\${response.status})\`;
            webAccessFormError.style.display = 'block';
        }
    } catch (error) {
        console.error('Error saving web access:', error);
        webAccessFormError.textContent = 'Ocurrió un error de red.';
        webAccessFormError.style.display = 'block';
    }
}

function editWebAccess(id) {
    openWebAccessModal(id);
}

async function deleteWebAccess(id) {
    if(confirm(\`¿Está seguro de eliminar acceso web ID: \${id}?\`)) {
        const token = localStorage.getItem('accessToken');
        try {
            const response = await fetch(\`\${API_BASE_URL}/web-accesses/\${id}\`, {
                method: 'DELETE',
                headers: { 'Authorization': \`Bearer \${token}\` }
            });
            if (response.ok) {
                showGlobalMessage('Acceso Web eliminado con éxito.');
                loadAccesos(); // Refresh table
            } else {
                if (response.status === 401) logout();
                const errorData = await response.json();
                showGlobalMessage(errorData.detail || 'Error al eliminar acceso web.', 'error');
            }
        } catch (error) {
            console.error('Error deleting web access:', error);
            showGlobalMessage('Ocurrió un error de red al eliminar.', 'error');
        }
    }
}

// Function to open User Registration Modal
function loadUserRegistrationForm() {
    updateMainHeader('Registrar Nuevo Usuario del Sistema');
    if (!userRegistrationModal || !userRegistrationForm || !userRegFormError) {
        console.error("User registration modal elements not found.");
        document.getElementById('contentArea').innerHTML = '<p>Error: Elementos del modal de registro no encontrados.</p>';
        return;
    }
    userRegistrationForm.reset();
    userRegFormError.style.display = 'none';
    userRegFormError.textContent = '';
    userRegistrationModal.style.display = 'block';
    // Unlike other modals, we don't load existing data here, it's always for new users.
    // The contentArea is not changed; the modal appears on top.
}

async function handleUserRegistrationFormSubmit(event) {
    event.preventDefault();
    if (!userRegFormError) return;
    userRegFormError.style.display = 'none';
    userRegFormError.textContent = '';

    const formData = getFormData(userRegistrationForm);

    // Client-side validation
    if (!formData.username || !formData.email || !formData.password || !formData.role) {
        userRegFormError.textContent = 'Todos los campos (Username, Email, Password, Rol) son obligatorios.';
        userRegFormError.style.display = 'block';
        return;
    }
    // Basic email validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(formData.email)) {
        userRegFormError.textContent = 'Por favor, ingrese un email válido.';
        userRegFormError.style.display = 'block';
        return;
    }

    const body = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: formData.role,
        full_name: formData.full_name || null
    };

    const token = localStorage.getItem('accessToken'); // Admin token

    try {
        const response = await fetch(\`\${API_BASE_URL}/auth/users/\`, { // Endpoint for creating users by admin
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': \`Bearer \${token}\`
            },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            if (userRegistrationModal) userRegistrationModal.style.display = 'none';
            showGlobalMessage('Usuario registrado con éxito.');
            // Optionally, if there's a user list view for admins, refresh it.
            // loadAdminUserList();
        } else {
            if (response.status === 401) logout(); // Admin token expired or invalid
            const errorData = await response.json();
            userRegFormError.textContent = errorData.detail || \`Error al registrar usuario (\${response.status})\`;
            userRegFormError.style.display = 'block';
        }
    } catch (error) {
        console.error('Error registering user:', error);
        userRegFormError.textContent = 'Ocurrió un error de red al registrar el usuario.';
        userRegFormError.style.display = 'block';
    }
}


// User Registration (Placeholder if not fully implemented above)
// function loadUserRegistrationForm() { updateMainHeader('Registrar Nuevo Usuario'); document.getElementById('contentArea').innerHTML = '<h2>Registrar Usuario</h2><p>Formulario de registro de usuarios (solo Admin) (TODO)...</p>'; }

function loadReportes() {
    updateMainHeader('Generación de Reportes');
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = \`
        <h2>Reportes</h2>
        <p>Descargue los reportes disponibles:</p>
        <ul>
            <li><a href="/export/excel/reporte_activos" target="_blank" rel="noopener noreferrer">Descargar Reporte General de Activos (Excel)</a></li>
            <li>
                <label for="actaEmployeeId">ID de Empleado para Acta:</label>
                <input type="number" id="actaEmployeeId" placeholder="Ingrese ID Empleado" style="padding: 5px; margin-right: 5px;">
                <button id="generateActaBtn" style="width:auto; padding: 5px 10px;">Generar/Ver Acta (HTML)</button>
                <p id="actaError" class="error-message" style="display:none;"></p>
            </li>
        </ul>
    \`;

    // Add event listener for the new button
    const generateActaBtn = document.getElementById('generateActaBtn');
    if(generateActaBtn) {
        generateActaBtn.addEventListener('click', () => {
            const employeeId = document.getElementById('actaEmployeeId').value;
            const actaError = document.getElementById('actaError');
            if(actaError) actaError.style.display = 'none'; // Clear previous errors

            if (!employeeId) {
                if(actaError) {
                    actaError.textContent = 'Por favor, ingrese un ID de empleado.';
                    actaError.style.display = 'block';
                } else {
                    alert('Por favor, ingrese un ID de empleado.');
                }
                return;
            }
            // Open acta.html in a new tab
            window.open(\`/acta.html?employee_id=\${employeeId}\`, '_blank');
        });
    }
}

// downloadActa function is no longer directly called by a button with this name
// The logic is now inside the event listener for generateActaBtn
/* function downloadActa() { // Old function, can be removed or kept if used elsewhere
    const employeeId = document.getElementById('employeeIdActa').value; // Ensure ID matches new HTML
    if (employeeId) {
        window.open(\`/export/word/acta_empleado/\${employeeId}\`, '_blank');
    } else {
        alert('Por favor, ingrese un ID de empleado.');
    }
}

function loadAnalisis() {
    updateMainHeader('Análisis de Datos');
    document.getElementById('contentArea').innerHTML = \`
        <h2>Visualizaciones</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
            <div style="flex: 1; min-width: 300px; max-width: 400px; padding:10px; border: 1px solid #eee; box-shadow: 0 0 5px rgba(0,0,0,0.1);">
                <h3>Activos por Tipo</h3>
                <img src="/analysis/charts/activos_por_tipo?_=\${new Date().getTime()}" alt="Activos por Tipo">
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 400px; padding:10px; border: 1px solid #eee; box-shadow: 0 0 5px rgba(0,0,0,0.1);">
                <h3>Empleados por Departamento</h3>
                <img src="/analysis/charts/empleados_por_departamento?_=\${new Date().getTime()}" alt="Empleados por Departamento">
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 400px; padding:10px; border: 1px solid #eee; box-shadow: 0 0 5px rgba(0,0,0,0.1);">
                <h3>Licencias por Software</h3>
                <img src="/analysis/charts/licencias_por_software?_=\${new Date().getTime()}" alt="Licencias por Software">
            </div>
        </div>
    \`;
}

// Ensure auth.js functions are available
// function logout() { localStorage.removeItem('accessToken'); localStorage.removeItem('tokenType'); window.location.href = '/'; }
// function getAuthToken() { return localStorage.getItem('accessToken'); }

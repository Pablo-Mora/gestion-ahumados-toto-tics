document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const employeeId = urlParams.get('employee_id');
    const actaContentDiv = document.getElementById('actaContent');
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');

    // Assumes auth.js is loaded and provides getAuthToken() or we access localStorage directly
    const token = localStorage.getItem('accessToken');

    if (!employeeId) {
        actaContentDiv.innerHTML = '<h1>ID de empleado no proporcionado.</h1><p>Por favor, acceda a esta página desde el dashboard.</p>';
        if (downloadPdfBtn) downloadPdfBtn.style.display = 'none';
        return;
    }
    if (!token) {
        actaContentDiv.innerHTML = '<h1>Acceso no autorizado.</h1><p>Por favor, inicie sesión y acceda a esta página desde el dashboard.</p>';
        if (downloadPdfBtn) downloadPdfBtn.style.display = 'none';
        // Consider redirecting: window.location.href = '/';
        return;
    }

    document.getElementById('currentDate').textContent = new Date().toLocaleDateString('es-ES', {
        year: 'numeric', month: 'long', day: 'numeric'
    });

    try {
        const empResponse = await fetch(\`/employees/\${employeeId}\`, {
            headers: { 'Authorization': \`Bearer \${token}\` }
        });
        if (!empResponse.ok) {
            if (empResponse.status === 401) logout(); // Assumes logout() is global from auth.js
            throw new Error(\`Error al cargar datos del empleado (\${empResponse.status}).\`);
        }
        const employee = await empResponse.json();

        document.getElementById('empNombre').textContent = employee.nombre;
        document.getElementById('empId').textContent = employee.identificacion;
        document.getElementById('empCargo').textContent = employee.cargo;
        document.getElementById('empDepto').textContent = employee.departamento || 'N/A';
        document.getElementById('empNombreFirma').textContent = employee.nombre;

        // Populate Hardware
        const hardwareTableBody = document.querySelector('#hardwareTable tbody');
        hardwareTableBody.innerHTML = ''; // Clear any placeholder rows
        if (employee.hardware_items && employee.hardware_items.length > 0) {
            employee.hardware_items.forEach(hw => {
                const row = hardwareTableBody.insertRow();
                row.insertCell().textContent = hw.tipo_equipo || 'N/A';
                row.insertCell().textContent = hw.marca || 'N/A';
                row.insertCell().textContent = hw.modelo || 'N/A';
                row.insertCell().textContent = hw.serial || 'N/A';
                row.insertCell().textContent = hw.notas || ''; // Using 'notas' as 'Observaciones'
            });
            document.getElementById('noHardwareMsg').style.display = 'none';
            document.getElementById('hardwareTable').style.display = '';
        } else {
            document.getElementById('noHardwareMsg').style.display = 'block';
            document.getElementById('hardwareTable').style.display = 'none';
        }

        // Populate Licenses
        const licenseTableBody = document.querySelector('#licenseTable tbody');
        licenseTableBody.innerHTML = ''; // Clear placeholder rows
        if (employee.licenses && employee.licenses.length > 0) {
            employee.licenses.forEach(lic => {
                const row = licenseTableBody.insertRow();
                row.insertCell().textContent = lic.software_nombre;
                let claveDisplay = "N/A";
                if (lic.clave_producto && lic.clave_producto.length > 4) {
                    claveDisplay = \`********\${lic.clave_producto.slice(-4)}\`;
                } else if (lic.clave_producto) {
                    claveDisplay = lic.clave_producto; // Show full if short or for other reasons
                }
                row.insertCell().textContent = claveDisplay;
                row.insertCell().textContent = lic.tipo_licencia;
                row.insertCell().textContent = lic.fecha_vencimiento ? new Date(lic.fecha_vencimiento).toLocaleDateString('es-ES') : 'N/A';
            });
            document.getElementById('noLicensesMsg').style.display = 'none';
            document.getElementById('licenseTable').style.display = '';
        } else {
            document.getElementById('noLicensesMsg').style.display = 'block';
            document.getElementById('licenseTable').style.display = 'none';
        }

    } catch (error) {
        console.error('Error populating acta:', error);
        actaContentDiv.innerHTML = \`<h1>Error al cargar datos para el acta: \${error.message}</h1><p>Intente recargar o contacte a soporte.</p>\`;
        if (downloadPdfBtn) downloadPdfBtn.style.display = 'none';
    }

    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', () => {
            const element = document.getElementById('actaContent');
            const opt = {
                margin:       [0.5, 0.5, 0.5, 0.5], // top, left, bottom, right in inches
                filename:     \`acta_entrega_emp\${employeeId}_\${new Date().toISOString().slice(0,10)}.pdf\`,
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true, logging: true },
                jsPDF:        { unit: 'in', format: 'A4', orientation: 'portrait' }
            };
            html2pdf().from(element).set(opt).save();
        });
    }
});

// Make logout available if called from an inline onclick in HTML from another page context
// This is not strictly needed if acta.html doesn't have a logout button itself.
// function logout() { localStorage.removeItem('accessToken'); localStorage.removeItem('tokenType'); window.location.href = '/'; }

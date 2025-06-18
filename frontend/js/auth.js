document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            loginError.style.display = 'none';
            loginError.textContent = ''; // Clear previous errors

            const username = loginForm.username.value;
            const password = loginForm.password.value;

            if (!username || !password) {
                loginError.textContent = 'Por favor, ingrese usuario y contraseña.';
                loginError.style.display = 'block';
                return;
            }

            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('accessToken', data.access_token);
                    localStorage.setItem('tokenType', data.token_type);
                    // Redirect to dashboard
                    window.location.href = '/dashboard'; // Make sure this route exists in FastAPI
                } else {
                    let errorMsg = 'Error de autenticación.'; // Default message
                    try {
                        const errorData = await response.json();
                        errorMsg = errorData.detail || errorMsg;
                    } catch (e) {
                        // If parsing error JSON fails, use the default or status text
                        errorMsg = response.statusText || errorMsg;
                    }
                    loginError.textContent = errorMsg;
                    loginError.style.display = 'block';
                }
            } catch (error) {
                console.error('Login error:', error);
                loginError.textContent = 'Ocurrió un error al intentar iniciar sesión.';
                loginError.style.display = 'block';
            }
        });
    }

    // General check for pages that require authentication
    // This is a client-side check and is mainly for UX.
    // Robust protection happens at the API level.
    const protectedPaths = ['/dashboard']; // Add other protected paths here
    const currentPath = window.location.pathname;

    if (protectedPaths.some(path => currentPath.startsWith(path))) {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            console.log("No token found, redirecting to login from auth.js general check.");
            // window.location.href = '/'; // Redirect to login
        }
    }
});

function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('tokenType');
    window.location.href = '/'; // Redirect to login page
}

// Function to get the auth token (if needed by other scripts)
function getAuthToken() {
    return localStorage.getItem('accessToken');
}

// Function to make authenticated API calls (example)
// async function fetchProtectedData(url, options = {}) {
//     const token = getAuthToken();
//     if (!token) {
//         console.error("No token available for authenticated request.");
//         // Optionally redirect to login
//         // window.location.href = '/';
//         return null;
//     }

//     const headers = {
//         ...options.headers,
//         'Authorization': `Bearer ${token}`,
//     };

//     const response = await fetch(url, { ...options, headers });

//     if (response.status === 401) { // Unauthorized
//         console.warn("Unauthorized request. Token might be expired or invalid.");
//         logout(); // Force logout
//         return null;
//     }
//     return response;
// }

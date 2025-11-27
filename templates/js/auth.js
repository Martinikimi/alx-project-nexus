// Authentication Functions
document.getElementById('loginFormElement').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };

    try {
        const response = await fetch(`${AUTH_API}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            showMessage('loginMessage', '✅ Login successful!', 'success');
            
            setTimeout(() => {
                navigateTo('/');
            }, 1000);
        } else {
            showMessage('loginMessage', `❌ Error: ${data.error || JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        showMessage('loginMessage', `❌ Network error: ${error.message}`, 'error');
    }
});

document.getElementById('registerFormElement').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        email: document.getElementById('regEmail').value,
        username: document.getElementById('regUsername').value,
        first_name: document.getElementById('regFirstName').value,
        last_name: document.getElementById('regLastName').value,
        phone_number: document.getElementById('regPhone').value,
        date_of_birth: document.getElementById('regDob').value,
        address: document.getElementById('regAddress').value,
        password: document.getElementById('regPassword').value,
        password_confirm: document.getElementById('regPasswordConfirm').value
    };

    if (formData.password !== formData.password_confirm) {
        showMessage('registerMessage', '❌ Passwords do not match!', 'error');
        return;
    }

    try {
        const response = await fetch(`${AUTH_API}/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            showMessage('registerMessage', '✅ Registration successful!', 'success');
            
            setTimeout(() => {
                navigateTo('/');
            }, 1000);
        } else {
            showMessage('registerMessage', `❌ Error: ${JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        showMessage('registerMessage', `❌ Network error: ${error.message}`, 'error');
    }
});

async function loadProfile() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        navigateTo('/login');
        return;
    }

    try {
        const response = await fetch(`${AUTH_API}/profile/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const userData = await response.json();
            document.getElementById('profileData').innerHTML = `
                <div class="grid-2">
                    <div class="form-group">
                        <label><i class="fas fa-envelope"></i> Email:</label>
                        <input type="email" value="${userData.email}" readonly>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> Username:</label>
                        <input type="text" value="${userData.username}" readonly>
                    </div>
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> First Name:</label>
                        <input type="text" value="${userData.first_name}" readonly>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> Last Name:</label>
                        <input type="text" value="${userData.last_name}" readonly>
                    </div>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-phone"></i> Phone:</label>
                    <input type="text" value="${userData.phone_number || 'Not provided'}" readonly>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-birthday-cake"></i> Date of Birth:</label>
                    <input type="text" value="${userData.date_of_birth || 'Not provided'}" readonly>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-home"></i> Address:</label>
                    <textarea rows="3" readonly>${userData.address || 'Not provided'}</textarea>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-calendar-alt"></i> Age:</label>
                    <input type="text" value="${userData.age || 'Not available'}" readonly>
                </div>
            `;
        } else {
            await refreshToken();
            loadProfile();
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        document.getElementById('profileData').innerHTML = `<div class="error">❌ Error loading profile</div>`;
    }
}

async function logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    try {
        await fetch(`${AUTH_API}/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ refresh: refreshToken })
        });
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigateTo('/login');
    }
}
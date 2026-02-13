function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

function validatePassword(password) {
    // Keep same rules as registration (adjust if your login allows weaker rules)
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChars = /[!@#$%^&*]/.test(password);
    
    return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChars;
}

function validateLoginForm() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';

    if (!validateEmail(email)) {
        errorMessage.textContent += 'Invalid email format.\n';
    }
    if (!validatePassword(password)) {
        errorMessage.textContent += 'Password must be at least 8 characters long and include uppercase, lowercase, numbers, and special characters.\n';
    }

    return errorMessage.textContent === '';
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const errorMessage = document.getElementById('error-message');

        if (!validateLoginForm()) {
            alert('Please fix the errors in the form.');
            return;
        }

        const payload = {
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value
        };

        try {
            const res = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (res.ok) {
                // on success redirect or show success UI
                window.location.href = data.redirect || '/dashboard';
            } else {
                errorMessage.textContent = data.message || 'Login failed.';
            }
        } catch (err) {
            errorMessage.textContent = 'Server error. Please try again.';
        }
    });
});

document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const inviteCode = document.getElementById('invite_code').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    const payload = {
        username: username,
        password: password,
        invite_code: inviteCode
    };

    try {
        const response = await fetch('http://localhost:12308/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        window.location.href = '../login';
    } catch (error) {
        console.error('Error:', error);
        displayErrorMessage('Registration failed. Please try again.');
    }
});

function displayErrorMessage(message) {
    const errorMessage = document.createElement('p');
    errorMessage.textContent = message;
    errorMessage.style.color = 'red';
    errorMessage.style.fontWeight = 'bold';

    const form = document.getElementById('registerForm');
    form.appendChild(errorMessage);
}
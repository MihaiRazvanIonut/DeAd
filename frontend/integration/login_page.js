const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:12309/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Invalid Credentials');
        }
        const data = await response.json();
        const sessionId = data.session_id;

        setCookie('seshhid-ddeeaadd', sessionId, 1)
        window.location.href = 'http://localhost:12999/actions';
    } catch (error) {
        console.error('Error:', error);
        displayErrorMessage('Invalid Credentials');
    }
});

function setCookie(name, value, days) {
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + days);

    const expires = `expires=${expirationDate.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}


function displayErrorMessage(message) {
    const errorMessage = document.createElement('p');
    errorMessage.textContent = message;
    errorMessage.style.color = 'red';
    errorMessage.style.fontWeight = 'bold';

    const form = document.getElementById('loginForm');
    form.appendChild(errorMessage);
}
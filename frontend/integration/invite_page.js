function getCookie(name) {
    let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) return match[2];
    return null;
}
async function fetchAndDisplayInvites() {
    const sessionId = getCookie('seshhid-ddeeaadd');
    if (!sessionId) {
        console.error('Session ID not found in cookies.');
        return;
    }

    try {

        let response = await fetch(`http://localhost:12307/${sessionId}`);
        if (!response.ok) {
            console.error('Failed to fetch user ID.');
            return;
        }

        let data = await response.json();
        const userId = data.user_id;


        response = await fetch(`http://localhost:12302/${userId}`);
        if (!response.ok) {
            console.error('Failed to fetch invites.');
            return;
        }

        data = await response.json();
        const invites = data.invites;


        const tableBody = document.getElementById('invitesTableBody');
        tableBody.innerHTML = ''

        invites.forEach(invite => {
            const row = document.createElement('tr');
            row.className = 'default-table__row';
            row.tabIndex = 0;

            row.innerHTML = `
                <td>${invite.id}</td>
                <td>${invite.expiry_date ? invite.expiry_date : 'None'}</td>
                <td>${invite.status === 1 ? 'Claimed' : 'Unclaimed'}</td>
                <td>${invite.admin ? 'Yes' : 'No'}</td>
            `;

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}
async function handleGenerateInvite(event) {
    event.preventDefault();
    const adminInvite = document.getElementById('admin_invite').checked;
    const sessionId = getCookie('seshhid-ddeeaadd');
    if (!sessionId) {
        console.error('Session ID not found in cookies.');
        return;
    }

    try {
    
        let response = await fetch(`http://localhost:12307/${sessionId}`);
        if (!response.ok) {
            console.error('Failed to fetch user ID.');
            displayErrorMessage("You are not an admin or you have generated more than unclaimed 6 invites")
            return;
        }

        let data = await response.json();
        const userId = data.user_id;

    
        response = await fetch(`http://localhost:12302/?admin=${adminInvite}`, {
            method: 'POST',
            headers: {
                'x-user-id': userId
            }
        });

        if (!response.ok) {
            if (response.status === 403) {
                console.error('User is not an admin, cannot generate invite.');
                displayErrorMessage("You are not an admin")
            } else {
                console.error('Too many invites generated');
                displayErrorMessage("Too many invites generated that are not claimed")
            }
            return;
        }

        console.log('Invite generated successfully.');
        fetchAndDisplayInvites();
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayErrorMessage(message) {
    const errorMessage = document.createElement('p');
    errorMessage.textContent = message;
    errorMessage.style.color = 'red';
    errorMessage.style.fontWeight = 'bold';

    const form = document.getElementById('generateInviteForm');
    form.appendChild(errorMessage);
}

document.getElementById('generateInviteForm').addEventListener('submit', handleGenerateInvite);
window.onload = fetchAndDisplayInvites;
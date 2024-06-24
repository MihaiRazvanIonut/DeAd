async function fetchAndDisplayMyActions() {
    try {
        
        const getSessionIdFromCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        };
        const sessionId = getSessionIdFromCookie('seshhid-ddeeaadd');
        if (!sessionId) {
            console.error('Session ID not found in cookies');
            return;
        }

        
        const userIdResponse = await fetch(`http://localhost:12307/${sessionId}`);
        if (!userIdResponse.ok) {
            console.error('Failed to fetch user ID');
            return;
        }
        const userIdData = await userIdResponse.json();
        const userId = userIdData.user_id;
        
        
        const actionsResponse = await fetch(`http://localhost:12306/${userId}`);
        if (!actionsResponse.ok) {
            console.error('Failed to fetch user actions');
            return;
        }
        const actionsData = await actionsResponse.json();
        const actions = actionsData.actions;

        
        actions.sort((a, b) => new Date(b.time) - new Date(a.time));

        
        const tableBody = document.getElementById('myActionsTableBody');
        tableBody.innerHTML = ''; 

        actions.forEach(action => {
            const row = document.createElement('tr');
            row.className = 'default-table__row';
            row.tabIndex = 0;

            row.innerHTML = `
                <td>${action.visit_id}</td>
                <td>${action.type.charAt(0).toUpperCase() + action.type.slice(1)}</td>
                <td>${new Date(action.time).toLocaleString()}</td>
            `;

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchAndDisplayMyActions);

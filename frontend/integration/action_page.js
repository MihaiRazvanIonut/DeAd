async function fetchAndDisplayUserActions() {
    try {
    
        const response = await fetch('http://localhost:12306/');
        if (!response.ok) {
            console.error('Failed to fetch user actions.');
            return;
        }

        const data = await response.json();

        if (Array.isArray(data.actions)) {
            data.actions.sort((a, b) => new Date(b.time) - new Date(a.time));

        
            const tableBody = document.getElementById('userActionsTableBody');
            tableBody.innerHTML = '';

            data.actions.forEach(action => {
                const row = document.createElement('tr');
                row.className = 'default-table__row';
                row.tabIndex = 0;

                row.innerHTML = `
                    <td>${action.visit_id}</td>
                    <td>${action.type.charAt(0).toUpperCase() + action.type.slice(1)}</td>
                    <td>${action.username}</td>
                    <td>${new Date(action.time).toLocaleString()}</td>
                `;

                tableBody.appendChild(row);
            });
        } else {
            console.error('Data is not an array:', data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchAndDisplayUserActions);

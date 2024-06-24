document.addEventListener('DOMContentLoaded', () => {
    fetchVisits();

    const searchForm = document.querySelector('.search-box');
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const filterField = document.getElementById('filter').value;
        const searchValue = searchForm.querySelector('input[name="search"]').value;
        fetchVisits(filterField, searchValue);
    });
});

async function fetchVisits(field = null, value = null) {
    let url = 'http://localhost:12304/';
    if (field && value) {
        url += `?field=${field}&value=${value}`;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (data.visits && Array.isArray(data.visits)) {
            data.visits.sort((a, b) => new Date(a.date) - new Date(b.date));
            displayVisits(data.visits);
        }
    } catch (error) {
        console.error('Error fetching visits:', error);
    }
}

function displayVisits(visits) {
    const tableBody = document.querySelector('.default-table');
    tableBody.innerHTML = `
        <tr class="default-table__header">
            <th>ID</th>
            <th>Hyperlink</th>
            <th>Purpose</th>
            <th>Date</th>
        </tr>
    `;

    visits.forEach(visit => {
        const row = document.createElement('tr');
        row.classList.add('default-table__row');
        row.setAttribute('tabindex', '0');

        row.innerHTML = `
            <td>${visit.id}</td>
            <td><a href="http://localhost:12999/visits/${visit.id}" class="default-table__link">Link</a></td>
            <td>${visit.purpose.charAt(0).toUpperCase() + visit.purpose.slice(1)}</td>
            <td>${visit.date}</td>
        `;

        tableBody.appendChild(row);
    });
}

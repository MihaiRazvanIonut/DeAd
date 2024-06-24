document.addEventListener('DOMContentLoaded', function() {
    const prisonersTableBody = document.getElementById('prisonersTableBody');
    const searchForm = document.querySelector('.search-box');

    function displayPrisoners(prisoners) {
        prisonersTableBody.innerHTML = '';

        prisoners.forEach(prisoner => {
            const row = document.createElement('tr');
            row.classList.add('default-table__row');

            row.innerHTML = `
                <td>${prisoner.id}</td>
                <td><a href="http://localhost:12999/prisoners/${prisoner.id}" class="default-table__link">Link</a></td>
                <td>${prisoner.case_number}</td>
                <td>${prisoner.release_date}</td>
            `;

            prisonersTableBody.appendChild(row);
        });
    }

    function filterPrisoners(prisoners, filterOption, searchTerm) {
        if (!prisoners || !Array.isArray(prisoners)) {
            return [];
        }
        searchTerm = searchTerm.toLowerCase().trim();

        return prisoners.filter(prisoner => {
            if (filterOption === 'id') {
                return prisoner.id && prisoner.id.toString().toLowerCase().includes(searchTerm);
            } else if (filterOption === 'case_number') {
                if (typeof prisoner.case_number === 'string' || typeof prisoner.case_number === 'number') {
                    return prisoner.case_number.toString().toLowerCase().includes(searchTerm);
                }
                return false;
            } else if (filterOption === 'release_date') {
                return prisoner.release_date && prisoner.release_date.includes(searchTerm);
            }
            return false;
        });
    }

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const filterOption = document.getElementById('filter').value;
        const searchTerm = document.querySelector('.search-box__input[name="search"]').value.trim().toLowerCase();

        fetch('http://localhost:12300/')
            .then(response => response.json())
            .then(data => {
                console.log(data);

                if (data && data.prisoners && Array.isArray(data.prisoners)) {
                    const filteredPrisoners = filterPrisoners(data.prisoners, filterOption, searchTerm);
                    displayPrisoners(filteredPrisoners);
                } else {
                    console.error('Data recieved are not in the correct format', data);
                }
            })
            .catch(error => console.error('Error at getting prisoners data', error));
    });

    fetch('http://localhost:12300/')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            if (data && data.prisoners && Array.isArray(data.prisoners)) {
                displayPrisoners(data.prisoners);
            } else {
                console.error('Data recieved are not in the correct format', data);
            }
        })
        .catch(error => console.error('Error at getting prisoners data', error));
});


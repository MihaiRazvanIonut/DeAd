document.addEventListener('DOMContentLoaded', () => {
    const visitId = getVisitIdFromUrl();
    if (visitId) {
        fetchVisitData(visitId).then(visitData => populateForm(visitData));
    }
});

function getVisitIdFromUrl() {
    const url = new URL(window.location.href);
    const pathSegments = url.pathname.split('/');
    return pathSegments[pathSegments.length - 1];
}

async function fetchVisitData(visitId) {
    const response = await fetch(`http://localhost:12304/${visitId}`);
    if (response.ok) {
        return await response.json();
    } else {
        console.error(`Failed to fetch visit data for visit ID ${visitId}`);
    }
}

function populateForm(data) {
    console.log(data)
    document.getElementById('visit_title').textContent = `Visit #${data.id}`;
    document.getElementById('prisoner_id').value = data.prisoner_id;
    document.getElementById('visit_date').value = formatDate(data.date);
    document.getElementById('visit_start_time').value = formatTime(data.start_time);
    document.getElementById('visit_end_time').value = formatTime(data.end_time);
    document.getElementById('visit_purpose').value = data.purpose;
    document.getElementById('items_given').value = getItems(data.items, 1);
    document.getElementById('items_received').value = getItems(data.items, 0);
    document.getElementById('restricted_visit_checkbox').checked = data.restricted;
    if (data.restricted === true) {
        let summaryField = document.getElementById('summary');
        let summaryLabel = document.getElementById('summary_label');
        summaryField.style.display = 'none';
        summaryLabel.style.display = 'none';
    } else {
        document.getElementById('summary').value = data.summary;
    }
    document.getElementById('arousal').value = data.mood.arousal;
    document.getElementById('flow').value = data.mood.flow;
    document.getElementById('control').value = data.mood.control;
    document.getElementById('relaxation').value = data.mood.relaxation;

    populateVisitors(data.visitors);
}

function getItems(items, action) {
    return items.filter(item => item.action === action).map(item => item.name).join(', ');
}

function populateVisitors(visitors) {
    const visitorsFieldset = document.getElementById('visitors_fieldset');
    const witnessesFieldset = document.getElementById('witnesses_fieldset');
    visitorsFieldset.innerHTML = '<legend>Visitor/s</legend>';
    witnessesFieldset.innerHTML = '<legend>Witness/es</legend>';
    witnesses_count = 0;
    visitor_count = 0;
    visitors.forEach((person, index) => {
        person.visit_role === 1 ? index = visitor_count++ : index = witnesses_count++; 
        const personDiv = document.createElement('div');
        personDiv.className = 'default-form__fieldset';
        personDiv.innerHTML = `
            <label>${person.visit_role === 1 ? `Visitor ${index + 1}` : `Witness ${index + 1}`}</label>
            <label for="${person.visit_role === 1 ? 'visitor' : 'witness'}_first_name_${index}">
                First name:
            </label>
            <input type="text" id="${person.visit_role === 1 ? 'visitor' : 'witness'}_first_name_${index}" class="default-form__input" value="${person.first_name}" readonly>
            <label for="${person.visit_role === 1 ? 'visitor' : 'witness'}_last_name_${index}">
                Last name:
            </label>
            <input type="text" id="${person.visit_role === 1 ? 'visitor' : 'witness'}_last_name_${index}" class="default-form__input" value="${person.last_name}" readonly>
            <label for="${person.visit_role === 1 ? 'visitor' : 'witness'}_ssn_${index}">
                SSN
            </label>
            <input type="text" id="${person.visit_role === 1 ? 'visitor' : 'witness'}_ssn_${index}" class="default-form__input" value="${person.nin}" readonly>
            ${person.visit_role === 1 ? `
            <label for="visitor_relationship_${index}">Relationship with the prisoner:</label>
            <select id="visitor_relationship_${index}" class="default-form__input" disabled>
                <option value="spouse" ${person.relationship === 'spouse' ? 'selected' : ''}>Spouse</option>
                <option value="parent" ${person.relationship === 'parent' ? 'selected' : ''}>Parent</option>
                <option value="sibling" ${person.relationship === 'sibling' ? 'selected' : ''}>Sibling</option>
                <option value="child" ${person.relationship === 'child' ? 'selected' : ''}>Child</option>
                <option value="otherFamily" ${person.relationship === 'otherFamily' ? 'selected' : ''}>Other Family Member</option>
                <option value="friend" ${person.relationship === 'friend' ? 'selected' : ''}>Friend</option>
                <option value="legalRep" ${person.relationship === 'legalRep' ? 'selected' : ''}>Legal Representative</option>
                <option value="professional" ${person.relationship === 'professional' ? 'selected' : ''}>Professional (e.g., counselor, social worker)</option>
                <option value="educator" ${person.relationship === 'educator' ? 'selected' : ''}>Educator</option>
                <option value="community" ${person.relationship === 'community' ? 'selected' : ''}>Community Member</option>
                <option value="media" ${person.relationship === 'media' ? 'selected' : ''}>Media Representative</option>
                <option value="official" ${person.relationship === 'official' ? 'selected' : ''}>Government Official</option>
            </select>` : ''}
        `;
        if (person.visit_role === 1) {
            visitorsFieldset.appendChild(personDiv);
        } else {
            witnessesFieldset.appendChild(personDiv);
        }
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
}

function formatTime(timeString) {
    const date = new Date(timeString);
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    const minutesFormatted = minutes < 10 ? '0' + minutes : minutes;
    return `${hours}:${minutesFormatted} ${ampm}`;
}

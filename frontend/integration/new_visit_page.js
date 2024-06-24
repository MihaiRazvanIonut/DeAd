document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.default-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        await submitForm();
    });

});

async function submitForm() {
    const sessionId = getCookie('seshhid-ddeeaadd');
    if (!sessionId) {
        alert('Session ID not found. Please log in again.');
        return;
    }

    try {
        const userId = await getUserId(sessionId);
        const formData = getFormData();
        const visitData = constructVisitData(formData);
        await postVisitData(visitData, userId);
        window.location.href = 'http://localhost:12999/visits';
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Failed to submit the form. Please try again.');
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

async function getUserId(sessionId) {
    const response = await fetch(`http://localhost:12307/${sessionId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch user ID');
    }
    const data = await response.json();
    return data.user_id;
}

function getFormData() {
    const formData = {};
    formData.prisoner_id = document.getElementById('prisoner_id').value;
    formData.visitors = getVisitorsData();
    formData.date = document.getElementById('visit_date').value;
    formData.start_time = document.getElementById('visit_start_time').value;
    formData.end_time = document.getElementById('visit_end_time').value;
    formData.purpose = document.getElementById('visitPurpose').value;
    formData.items = getItemsData();
    formData.restricted = document.getElementById('restricted_visit_checkbox').checked;
    formData.summary = formData.restricted ? null : document.getElementById('summary').value;
    formData.mood = getMoodData();
    return formData;
}

function getVisitorsData() {
    const visitors = [];
    const visitorElements = document.querySelectorAll('#visitors_fieldset > div');
    visitorElements.forEach((element, index) => {
        const visitor = {
            first_name: element.querySelector(`#visitor_first_name_${index + 1}`).value,
            last_name: element.querySelector(`#visitor_last_name_${index + 1}`).value,
            nin: element.querySelector(`#visitor_ssn_${index + 1}`).value,
            relationship: element.querySelector(`#visitor_relationship_${index + 1}`).value,
            visit_role: 1
        };
        visitors.push(visitor);
    });

    const witnessElements = document.querySelectorAll('#witnesses_fieldset > div');
    witnessElements.forEach((element, index) => {
        const witness = {
            first_name: element.querySelector(`#witness_first_name`).value,
            last_name: element.querySelector(`#witness_last_name`).value,
            nin: element.querySelector(`#witness_ssn`).value,
            relationship: null,
            visit_role: 0
        };
        visitors.push(witness);
    });

    return visitors;
}

function getItemsData() {
    const items = [];
    const itemsGiven = document.getElementById('items_given').value.split(',');
    itemsGiven.forEach(item => {
        items.push({ name: item.trim(), action: 1 });
    });
    const itemsReceived = document.getElementById('items_received').value.split(',');
    itemsReceived.forEach(item => {
        items.push({ name: item.trim(), action: 0 });
    });
    return items;
}

function getMoodData() {
    return {
        arousal: parseInt(document.getElementById('arousal').value),
        flow: parseInt(document.getElementById('flow').value),
        control: parseInt(document.getElementById('control').value),
        relaxation: parseInt(document.getElementById('relaxation').value)
    };
}

function constructVisitData(formData) {
    return {
        prisoner_id: formData.prisoner_id,
        visitors: formData.visitors,
        date: formData.date,
        start_time: formatTimestamp(formData.date, formData.start_time),
        end_time: formatTimestamp(formData.date, formData.end_time),
        purpose: formData.purpose,
        items: formData.items,
        restricted: formData.restricted,
        summary: formData.summary,
        mood: formData.mood
    };
}

function formatTimestamp(date, time) {
    return `${date} ${time}:00.000`;
}

async function postVisitData(visitData, userId) {
    const response = await fetch('http://localhost:12304/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-user-id': userId
        },
        body: JSON.stringify(visitData)
    });

    if (!response.ok) {
        throw new Error('Failed to submit visit data');
    }
}

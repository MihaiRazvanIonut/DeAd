document.addEventListener('DOMContentLoaded', () => {
    const visitForm = document.getElementById('visits_form');
    visitForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const sessionId = getCookie('seshhid-ddeeaadd');
        if (!sessionId) {
            alert('Session ID is missing.');
            return;
        }

        try {
            const userId = await fetchUserId(sessionId);
            const formData = parseFormData();
            const visitId = getVisitIdFromUrl();

            const response = await sendVisitData(userId, visitId, formData);
            if (response.ok) {
                window.location.href = 'http://localhost:12999/visits';
            } else {
                alert('Failed to submit the form. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    async function fetchUserId(sessionId) {
        const response = await fetch(`http://localhost:12307/${sessionId}`);
        const data = await response.json();
        return data.user_id;
    }

    function parseFormData() {
        const visitDate = document.getElementById('visit_date').value;
        const startTime = document.getElementById('visit_start_time').value;
        const visitStartTime = formatTimestamp(visitDate, startTime);
        const endTime = document.getElementById('visit_end_time').value;
        const visitEndTime = formatTimestamp(visitDate, endTime);
        const visitPurpose = document.getElementById('visit_purpose').value;
        const itemsGiven = document.getElementById('items_given').value.split(',').map(item => ({ name: item.trim(), action: 1 }));
        const itemsReceived = document.getElementById('items_received').value.split(',').map(item => ({ name: item.trim(), action: 0 }));
        const restricted = document.getElementById('restricted_visit_checkbox').checked;
        const summary = restricted ? null : document.getElementById('summary').value;

        const mood = {
            arousal: parseInt(document.getElementById('arousal').value),
            flow: parseInt(document.getElementById('flow').value),
            control: parseInt(document.getElementById('control').value),
            relaxation: parseInt(document.getElementById('relaxation').value)
        };

        const visitorsFieldset = document.getElementById('visitors_fieldset');
        const witnessesFieldset = document.getElementById('witnesses_fieldset');

        const visitors = [];
        [...visitorsFieldset.children].forEach((child, index) => {
            if (index !== 0) {
            if (child.classList.contains('default-form__fieldset')) {
                visitors.push({
                    first_name: document.getElementById(`visitor_first_name_${index - 1}`).value,
                    last_name: document.getElementById(`visitor_last_name_${index - 1}`).value,
                    nin: document.getElementById(`visitor_ssn_${index - 1}`).value,
                    relationship: document.getElementById(`visitor_relationship_${index - 1}`).value,
                    visit_role: 1
                });
            }
        }
        });
        [...witnessesFieldset.children].forEach((child, index) => {
            if (index !== 0) {
            if (child.classList.contains('default-form__fieldset')) {
                visitors.push({
                    first_name: document.getElementById(`witness_first_name_${index - 1}`).value,
                    last_name: document.getElementById(`witness_last_name_${index - 1}`).value,
                    nin: document.getElementById(`witness_ssn_${index - 1}`).value,
                    relationship: null,
                    visit_role: 0
                });
            }
        }
        });
        return {
            date: visitDate,
            start_time: visitStartTime,
            end_time: visitEndTime,
            purpose: visitPurpose,
            items: [...itemsGiven, ...itemsReceived],
            restricted: restricted,
            summary: summary,
            mood: mood,
            visitors: visitors
        };
    }

    async function sendVisitData(userId, visitId, formData) {
        const response = await fetch(`http://localhost:12304/${visitId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'x-user-id': userId
            },
            body: JSON.stringify(formData)
        });
        return response;
    }
});

function formatTimestamp(date, time) {
    time = convertTo24Hour(time)
    return `${date} ${time}:00.000`;
}

function convertTo24Hour(time) {
    let [timePart, modifier] = time.split(' ');
    let [hours, minutes] = timePart.split(':');
    hours = parseInt(hours, 10);
    if (modifier === 'PM' && hours < 12) {
        hours += 12;
    }
    if (modifier === 'AM' && hours === 12) {
        hours = 0;
    }
    return `${hours.toString().padStart(2, '0')}:${minutes}`;
}


function getVisitIdFromUrl() {
    const url = new URL(window.location.href);
    const pathSegments = url.pathname.split('/');
    return pathSegments[pathSegments.length - 1];
}
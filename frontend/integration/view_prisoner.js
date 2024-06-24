let form_data = new FormData();

document.addEventListener('DOMContentLoaded', async function() {
    const url = window.location.href;
    const prisonerId = url.substring(url.lastIndexOf('/') + 1);

    console.log('Prisoner ID:', prisonerId);

    try {
        const response = await fetch(`http://localhost:12300/${prisonerId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch prisoner data');
        }

        const prisonerData = await response.json();
        console.log('Prisoner Data:', prisonerData);

        document.getElementById('prisoner_id').textContent = prisonerData.id;

        const prisonerFirstNameInput = document.getElementById('prisoner_first_name');
        const prisonerLastNameInput = document.getElementById('prisoner_last_name');
        const prisonerSSNInput = document.getElementById('prisoner_ssn');
        const prisonerBirthdayInput = document.getElementById('prisoner_birthday');
        const prisonerNationalityInput = document.getElementById('prisoner_nationality');
        const prisonerAddressInput = document.getElementById('prisoner_adress');
        const prisonerPhoneNumberInput = document.getElementById('prisoner_phone_number');
        const prisonerEmailInput = document.getElementById('prisoner_email');
        const emergencyPhoneNumberInput = document.getElementById('emergency_phone_number');
        const arrestDateInput = document.getElementById('arest_date');
        const convictionDateInput = document.getElementById('conviction_date');
        const crimeCommittedInput = document.getElementById('crime_commited');
        const courtCaseNumberInput = document.getElementById('court_case_number');
        const releaseDateInput = document.getElementById('release_date');
        const previousCrimesCommittedCheckbox = document.getElementById('previous_crimes_committed');

        if (prisonerFirstNameInput) {
            prisonerFirstNameInput.value = prisonerData.first_name;
        }
        if (prisonerLastNameInput) {
            prisonerLastNameInput.value = prisonerData.last_name;
        }
        if (prisonerSSNInput) {
            prisonerSSNInput.value = prisonerData.nin;
        }
        if (prisonerBirthdayInput) {
            prisonerBirthdayInput.value = prisonerData.date_of_birth;
        }
        if (prisonerNationalityInput) {
            prisonerNationalityInput.value = prisonerData.nationality;
        }
        if (prisonerAddressInput) {
            prisonerAddressInput.value = prisonerData.address;
        }
        if (prisonerPhoneNumberInput) {
            prisonerPhoneNumberInput.value = prisonerData.phone_number;
        }
        if (prisonerEmailInput) {
            prisonerEmailInput.value = prisonerData.email;
        }
        if (emergencyPhoneNumberInput) {
            emergencyPhoneNumberInput.value = prisonerData.emergency_contact;
        }
        if (arrestDateInput) {
            arrestDateInput.value = prisonerData.arrest_date;
        }
        if (convictionDateInput) {
            convictionDateInput.value = prisonerData.conviction_date;
        }
        if (crimeCommittedInput) {
            crimeCommittedInput.value = prisonerData.crime_committed;
        }
        if (courtCaseNumberInput) {
            courtCaseNumberInput.value = prisonerData.case_number;
        }
        if (releaseDateInput) {
            releaseDateInput.value = prisonerData.release_date;
        }
        if (previousCrimesCommittedCheckbox) {
            previousCrimesCommittedCheckbox.checked = prisonerData.repeated_felon;
        }

        const prisonerImagePreview = document.getElementById('prisoner_image_preview');
        const img = document.createElement('img');
        img.src = prisonerData.image;
        img.className = 'person-photo';
        prisonerImagePreview.appendChild(img);
    } catch (error) {
        console.error('Error fetching prisoner data:', error);
        alert('Failed to fetch prisoner data. Please try again.');
    }
});

document.getElementById('prisoners_form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const imageFile = form_data.get('prisoner_image');
    let imageUrl = '';
    if (imageFile && imageFile.size > 0) {
        const imageUploadResponse = await fetch(`http://localhost:12301/`, {
            method: 'POST',
            headers: {
                'Content-Type': imageFile.type
            },
            body: imageFile
        });
        
        if (imageUploadResponse.ok) {
            const imageUploadData = await imageUploadResponse.text();
            imageUrl = imageUploadData;
        } else {
            console.error('Image upload failed');
            return;
        }
    }
    
    const prisonerData = {
        nin: formData.get('prisoner_ssn'),
        first_name: formData.get('prisoner_first_name'),
        last_name: formData.get('prisoner_last_name'),
        date_of_birth: formData.get('prisoner_birthday'),
        nationality: formData.get('prisoner_nationality'),
        image: imageUrl,
        address: formData.get('prisoner_adress'),
        phone_number: formData.get('prisoner_phone_number'),
        email: formData.get('prisoner_email'),
        emergency_contact: formData.get('emergency_phone_number'),
        arrest_date: formData.get('arest_date'),
        conviction_date: formData.get('conviction_date'),
        crime_committed: formData.get('crime_commited'),
        case_number: Number(formData.get('court_case_number')),
        release_date: formData.get('release_date'),
        repeated_felon: formData.get('previous_crimes_committed') === 'on'
    };

    console.log(prisonerData);
    const url = window.location.href;
    const prisonerId = url.substring(url.lastIndexOf('/') + 1);
    
    try {
        const prisonerSubmitResponse = await fetch(`http://localhost:12300/${prisonerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(prisonerData)
        });
        
        if (prisonerSubmitResponse.ok) {
            console.log('Prisoner updated successfully');
            window.location.href = 'http://localhost:12999/prisoners';
        } else {
            console.error('Failed to update prisoner');
            alert('Failed to update prisoner. Please try again.');
        }
    } catch (error) {
        console.error('Error updating prisoner:', error);
        alert('Failed to update prisoner. Please try again.');
    }
});
function loadPrisonerImage(input) {
    const preview = document.getElementById('prisoner_image_preview');
    preview.innerHTML = ""; 
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.className = "person-photo";
            preview.appendChild(img);

            form_data.set('prisoner_image', file);
        };
        reader.readAsDataURL(file);
    }
}
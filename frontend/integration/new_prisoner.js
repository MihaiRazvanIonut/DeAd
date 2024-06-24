document.getElementById('prisonerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const requiredFields = form.querySelectorAll('input[required], textarea[required]');
    let allFieldsFilled = true;
    requiredFields.forEach(field => {
        if (!field.value) {
            allFieldsFilled = false;
        }
    });

    if (!allFieldsFilled) {
        alert('Please fill in all required fields.');
        return;
    }

    const imageFile = formData.get('prisoner_image');
    let imageUrl = '';
    if (imageFile && imageFile.size > 0) {
        const imageUploadResponse = await fetch('http://localhost:12301/', {
            method: 'POST',
            headers: {
                'Content-Type': imageFile.type
            },
            body: imageFile
        });
        
        if (imageUploadResponse.ok) {
            const imageUploadData = await imageUploadResponse.text();
            imageUrl = imageUploadData;
            console.log(imageUrl)
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
        address: formData.get('prisoner_address'),
        phone_number: formData.get('prisoner_phone_number'),
        email: formData.get('prisoner_email'),
        emergency_contact: formData.get('emergency_phone_number'),
        arrest_date: formData.get('arrest_date'),
        conviction_date: formData.get('conviction_date'),
        crime_committed: formData.get('crime_committed'),
        case_number: Number(formData.get('court_case_number')),
        release_date: formData.get('release_date'),
        repeated_felon: formData.get('previous_crimes_committed') === 'on'
    };
    const prisonerSubmitResponse = await fetch('http://localhost:12300/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(prisonerData)
    });
    console.log(prisonerSubmitResponse)
    if (prisonerSubmitResponse.ok) {
        console.log('Prisoner created successfully');
        window.location.href = 'http://localhost:12999/prisoners';
    } else {
        console.error('Failed to create prisoner');
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
        };
        reader.readAsDataURL(file);
    }
}
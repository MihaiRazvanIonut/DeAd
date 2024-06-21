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
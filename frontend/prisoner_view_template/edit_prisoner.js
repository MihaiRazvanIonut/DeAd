let form = document.getElementById("prisoners_form");
let prisonerImageInput = document.getElementById("prisoner_image");

function makeFormReadOnly() {
    let inputs = form.getElementsByClassName("default-form__input");
    let fileInputs = form.querySelectorAll("input[type='file']");

    [].forEach.call(inputs, function (input) {
        input.readOnly = true;
    });

    [].forEach.call(fileInputs, function (fileInput) {
        fileInput.disabled = true;
    });

    prisonerImageInput.style.display = 'none';
}

function makeFormEditable() {
    let inputs = form.getElementsByClassName("default-form__input");
    let fileInputs = form.querySelectorAll("input[type='file']");

    [].forEach.call(inputs, function (input) {
        input.readOnly = false;
    });

    [].forEach.call(fileInputs, function (fileInput) {
        fileInput.disabled = false;
    });

    prisonerImageInput.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    makeFormReadOnly();
});

function toggleEditMode() {
    let editButton = document.getElementById('editButton');
    let isEditable = editButton.textContent === 'Edit';

    if (isEditable) {
        makeFormEditable();
    } else {
        makeFormReadOnly();
    }
}

document.getElementById('editButton').addEventListener('click', toggleEditMode);

document.getElementById('saveDraftButton').addEventListener('click', function() {
    makeFormReadOnly();
    document.getElementById('editButton').textContent = 'Edit';
});

let form = document.getElementById("prisoners_form");

function readOnlyForm() {
    let inputs = form.getElementsByClassName("default-form__input");
    let fileInputs = form.querySelectorAll("input[type='file']");

    [].forEach.call(inputs, function (input) {
        console.log(input);
        input.readOnly = true;
    });

    [].forEach.call(fileInputs, function (fileInput) {
        console.log(fileInput);
        fileInput.disabled = true;
    });
}

function editForm() {
    let inputs = form.getElementsByClassName("default-form__input");
    let fileInputs = form.querySelectorAll("input[type='file']");

    [].forEach.call(inputs, function (input) {
        console.log(input);
        input.readOnly = false;
    });

    [].forEach.call(fileInputs, function (fileInput) {
        console.log(fileInput);
        fileInput.disabled = false;
    });
}
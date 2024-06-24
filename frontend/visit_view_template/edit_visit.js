let form = document.getElementById("visits_form");

function readOnlyForm() {
    let inputs = form.getElementsByClassName("default-form__input");
    let selects = form.getElementsByTagName("select");
    let fileInputs = form.querySelectorAll("input[type='checkbox']");
    
    [].forEach.call(inputs, function (input) {
        console.log(input);
        input.readOnly = true;
    });
    
    [].forEach.call(selects, function (select) {
        console.log(select);
        select.disabled = true;
    });
    
    [].forEach.call(fileInputs, function (fileInput) {
        console.log(fileInput);
        fileInput.disabled = true;
    });
}

function editForm() {
    let inputs = form.getElementsByClassName("default-form__input");
    let selects = form.getElementsByTagName("select");
    let fileInputs = form.querySelectorAll("input[type='checkbox']");
    
    [].forEach.call(inputs, function (input) {
        console.log(input);
        input.readOnly = false;
    });
    
    [].forEach.call(selects, function (select) {
        console.log(select);
        select.disabled = false;
    });
    
    [].forEach.call(fileInputs, function (fileInput) {
        console.log(fileInput);
        fileInput.disabled = false;
    });
}

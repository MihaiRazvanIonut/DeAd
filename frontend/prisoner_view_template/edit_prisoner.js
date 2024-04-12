let form = document.getElementById("prisoners_form");
function readOnlyForm() {
    let inputs = form.getElementsByClassName("default-form__input");
    [].forEach.call(inputs, function (input) {
        console.log(input);
        input.readOnly = true;
    });
} 

function editForm() {
    let inputs = form.getElementsByClassName("default-form__input");
    [].forEach.call(inputs, function (input) {
        console.log(input);
        input.readOnly = false;
    });
}
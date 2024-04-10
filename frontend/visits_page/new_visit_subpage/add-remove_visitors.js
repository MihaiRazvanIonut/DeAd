let visitorsCounter = 0;
let maxVisitors = 10;
const visitorsFieldset = document.getElementById("visitors_fieldset");

function addVisitor() {
    if (visitorsCounter == maxVisitors) {
        alert("You have reached the limit of visitors. There can be a maximum of " + maxVisitors);
    } else {
        let newVisitor = document.createElement('div');
        newVisitor.className = "default-form__fieldset";
        const visitorNum = visitorsCounter + 1;
        newVisitor.innerHTML = 
        `
        <label> Visitor ` + visitorNum + ` </label>
        <label for="visitor_first_name">
            First name:
        </label>
        <input type="text" id="visitor_first_name" class="default-form__input">    
        <label for="visitor_last_name">
           Last name:
        </label>
        <input type="text" id="visitor_last_name" class="default-form__input">
        <label for="visitor_ssn">
            SSN:
        </label>
        <input type="number" id="visitor_ssn" class="default-form__input">
        <label for="visitor_image">
            Image:
        </label>
        <input type="link" id="visitor_image" class="default-form__input">
        `;
        visitorsFieldset.appendChild(newVisitor);
        visitorsCounter++;
        console.log("Added visitor" + visitorsCounter);
    }
}

function removeVisitor() {
    if (visitorsCounter == 0) {
        alert("There are no visitors added!");
    } else {
        visitorsCounter--;
        visitorsFieldset.removeChild(visitorsFieldset.lastChild);
        console.log("Deleted visitor");
    }
}
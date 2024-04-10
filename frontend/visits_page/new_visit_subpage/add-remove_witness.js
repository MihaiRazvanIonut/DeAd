let witnessesCounter = 0;
let maxWitnesses = 3;
const witnessesFieldset = document.getElementById("witnesses_fieldset");

function addWitness() {
    if (witnessesCounter == maxWitnesses) {
        alert("You have reached the limit of witnesses. There can be a maximum of " + maxWitnesses);
    } else {
        let newWitness = document.createElement('div');
        newWitness.className = "visit_form__fieldset";
        const witnessNum = witnessesCounter + 1;
        newWitness.innerHTML = 
        `
        <label> Witness ` + witnessNum + ` </label>
        <label for="witness_first_name">
            First name:
        </label>
        <input type="text" id="witness_first_name" class="visit_form__input">    
        <label for="witness_last_name">
           Last name:
        </label>
        <input type="text" id="witness_last_name" class="visit_form__input">
        <label for="witness_ssn">
            SSN:
        </label>
        <input type="number" id="witness_ssn" class="visit_form__input">
        `;
        witnessesFieldset.appendChild(newWitness);
        witnessesCounter++;
        console.log("Added witness" + witnessesCounter);
    }
}

function removeWitness() {
    if (witnessesCounter == 0) {
        alert("There are no witnesses added!");
    } else {
        witnessesCounter--;
        witnessesFieldset.removeChild(witnessesFieldset.lastChild);
        console.log("Deleted witness");
    }
}
let maxWitnesses = 3;
const witnessesFieldset = document.getElementById("witnesses_fieldset");

function addWitness() {
    witnessesCounter = witnessesFieldset.children.length - 2
    if (witnessesCounter + 1 == maxWitnesses) {
        alert("You have reached the limit of witnesses. There can be a maximum of " + maxWitnesses);
    } else {
        let newWitness = document.createElement('div');
        newWitness.className = "default-form__fieldset";
        const witnessNum = witnessesCounter + 1;
        newWitness.innerHTML = 
        `
        <label> Witness ` + (1 + witnessNum) + ` </label>
        <label for="witness_first_name_${witnessNum}">
            First name:
        </label>
        <input type="text" id="witness_first_name_${witnessNum}" class="default-form__input" required>    
        <label for="witness_last_name_${witnessNum}">
           Last name:
        </label>
        <input type="text" id="witness_last_name_${witnessNum}" class="default-form__input" required>
        <label for="witness_ssn_${witnessNum}">
            SSN:
        </label>
        <input type="number" id="witness_ssn_${witnessNum}" class="default-form__input" required>
        `;
        witnessesFieldset.appendChild(newWitness);
        witnessesCounter++;
        console.log("Added witness " + witnessesCounter);
    }
}

function removeWitness() {
    if (witnessesCounter == 0) {
        alert("There are no witnesses added!");
    } else {
        witnessesCounter--;
        witnessesFieldset.removeChild(witnessesFieldset.lastElementChild);
        console.log("Deleted witness");
    }
}
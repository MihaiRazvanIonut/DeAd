let maxVisitors = 10;
const visitorsFieldset = document.getElementById("visitors_fieldset");

function addVisitor() {
    let visitorsCounter = visitorsFieldset.children.length - 2;

    if (visitorsCounter + 1 == maxVisitors) {
        alert("You have reached the limit of visitors. There can be a maximum of " + maxVisitors);
    } else {
        let newVisitor = document.createElement('div');
        newVisitor.className = "default-form__fieldset";
        const visitorNum = visitorsCounter + 1;
        newVisitor.innerHTML = 
        `
        <label> Visitor ` + (1 + visitorNum) + ` </label>
        <label for="visitor_first_name_` + visitorNum + `">
            First name:
        </label>
        <input type="text" id="visitor_first_name_` + visitorNum + `" class="default-form__input" required>    
        <label for="visitor_last_name_` + visitorNum + `">
           Last name:
        </label>
        <input type="text" id="visitor_last_name_` + visitorNum + `" class="default-form__input" required>
        <label for="visitor_ssn_` + visitorNum + `">
            SSN:
        </label>
        <input type="text" id="visitor_ssn_` + visitorNum + `" class="default-form__input" required>
        <label for="visitor_relationship_` + visitorNum + `">Relationship with the prisoner:</label>
            <select id="visitor_relationship_` + visitorNum + `" class="default-form__input" required>
                <option value="spouse">Spouse</option>
                <option value="parent">Parent</option>
                <option value="sibling">Sibling</option>
                <option value="child">Child</option>
                <option value="otherFamily">Other Family Member</option>
                <option value="friend">Friend</option>
                <option value="legalRep">Legal Representative</option>
                <option value="professional">Professional (e.g., counselor, social worker)</option>
                <option value="educator">Educator</option>
                <option value="community">Community Member</option>
                <option value="media">Media Representative</option>
                <option value="official">Government Official</option>
            </select>
        `;
        visitorsFieldset.appendChild(newVisitor);
        console.log("Added visitor " + (visitorsCounter + 1));
    }
}

function removeVisitor() {
    let visitorsCounter = visitorsFieldset.children.length;

    if (visitorsCounter == 0) {
        alert("There are no visitors added!");
    } else {
        visitorsFieldset.removeChild(visitorsFieldset.lastElementChild);
        console.log("Deleted visitor " + visitorsCounter);
    }
}

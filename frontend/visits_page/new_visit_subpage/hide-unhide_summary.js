document.getElementById('restricted_visit_checkbox').addEventListener('change', function() {
    var summaryField = document.getElementById('summary');
    var summaryLabel = document.getElementById('summary_label');
    if (this.checked) {
        summaryField.style.display = 'none';
        summaryLabel.style.display = 'none';
    } else {
        summaryField.style.display = 'block';
        summaryLabel.style.display = 'block';
    }
});
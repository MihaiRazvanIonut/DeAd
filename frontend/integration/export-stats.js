document.addEventListener('DOMContentLoaded', function(){
    const exportForm = document.getElementById('exportForm');
    if(exportForm){
        exportForm.addEventListener('submit', function(event){
            event.preventDefault();
            const prisonerId = document.getElementById('prisoner_id').value.trim();
            const statisticType = document.querySelector('input[name="statistic_type"]:checked').value;
            const exportFormat = document.querySelector('input[name="export_format"]:checked').value;
            console.log(`: ${exportFormat}`);
            let url;
            if(prisonerId){
                url = `http://localhost:12303/${statisticType}/${prisonerId}?format=${exportFormat}`;
            } else{
                url = `http://localhost:12303/${statisticType}?format=${exportFormat}`;
            }
            console.log(`${url}`);
            fetch(url)
                .then(response => {
                    const disposition = response.headers.get('Content-Disposition');
                    let filename = 'downloaded-file';
                    if (disposition && disposition.indexOf('attachment') !== -1) {
                        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        const matches = filenameRegex.exec(disposition);
                        if (matches != null && matches[1]) { 
                            filename = matches[1].replace(/['"]/g, '');
                        }
                    }

                    return response.blob().then(blob => ({ blob, filename }));
                })
                .then(({ blob, filename }) => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => console.error('Error downloading the file:', error));
        });
    } else{
        console.error('Form element not found');
    }
});
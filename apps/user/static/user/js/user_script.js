document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function(event) {
            const fileName = event.target.files[0] ? event.target.files[0].name : 'Файл не вибрано';
            fileNameDisplay.textContent = fileName;
        });
    }
});
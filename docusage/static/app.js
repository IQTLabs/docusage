const dropArea = document.getElementById('dragDropArea');
const fileInput = document.getElementById('fileInput');

// Handle drag events
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.style.border = '2px dashed #205c5a';
});

dropArea.addEventListener('dragleave', (e) => {
    dropArea.style.border = '2px dashed #ccc';
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    dropArea.style.border = '2px dashed #ccc';
});

// Handle click event
dropArea.addEventListener('click', (e) => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    console.log(fileInput.files);
});

document.getElementById('createReport').addEventListener('click', (e) => {
    console.log('create report');
});


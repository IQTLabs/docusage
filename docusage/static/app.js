const dropArea = document.getElementById('dragDropArea');
const fileInput = document.getElementById('fileInput');

// Array to hold the files
let filesArray = [];

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
    addFiles(e.dataTransfer.files);
    dropArea.style.border = '2px dashed #ccc';
});

// Handle click event
dropArea.addEventListener('click', (e) => {
    fileInput.click();
});

// Handle file input change event
fileInput.addEventListener('change', (e) => {
    addFiles(e.target.files);
});

// Add files to drop area div
const addFiles = (files) => {
    Array.from(files).forEach(file => {
        // Check if file with the same name already exists in the array
        if (!filesArray.some(f => f.name === file.name)) {
            filesArray.push(file);
        }
    });

    dropArea.innerHTML = '';

    filesArray.forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.textContent = `📄 ${index + 1}: ${file.name}`;
        dropArea.appendChild(fileDiv);
    });
};

document.getElementById('createReport').addEventListener('click', async (e) => {
    const contentarea = document.getElementById('content');
    const spinner = document.getElementsByClassName('spinner')[0];

    contentarea.style.filter = 'blur(3px)';
    contentarea.style.pointerEvents = 'none';
    spinner.style.display = 'block';


    const formData = new FormData();
    filesArray.forEach((file, index) => {
        formData.append("files", file);
    });
    const mission = document.getElementById('missionInput').value;
    if (mission !== '') {
        formData.append("mission", mission);
    }
    const response = await fetch('/create_report', {
        method: 'POST',
        body: formData,
    });

    contentarea.style.filter = 'none';
    contentarea.style.pointerEvents = 'auto';
    spinner.style.display = 'none';

    if (!response.ok) {
        console.error('Report creation failed');
        return;
    }

    const report = await response.json();
    const reportArea = document.getElementById('reportContent');
    reportArea.textContent = report.content;
});
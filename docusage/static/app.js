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

// Handle file input change event
fileInput.addEventListener('change', (e) => {
    dropArea.innerHTML = '';

    Array.from(fileInput.files).forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.textContent = `📄 ${index + 1}: ${file.name}`;
        dropArea.appendChild(fileDiv);
    });
});

document.getElementById('createReport').addEventListener('click', async (e) => {
    const formData = new FormData();
    Array.from(fileInput.files).forEach((file, index) => {
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

    if (!response.ok) {
        console.error('Report creation failed');
        return;
    }

    const report = await response.json();
    const reportArea = document.getElementById('reportContent');
    reportArea.textContent = report.content;
});
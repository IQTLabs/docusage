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

    document.getElementById('createReport').disabled = false;
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
    if (mission.trim() !== '') {
        formData.append("mission", mission);
    }
    const reportSize = document.getElementById('sizeSelect').value;
    formData.append("reportSize", reportSize);

    const dynamicHeadersCheckbox = document.getElementById('dynamicCheckbox');
    if (dynamicHeadersCheckbox.checked) {
        formData.append("dynamicHeaders", "true");
    } else {
        formData.append("dynamicHeaders", "false");
    }
    const response = await fetch('/create_report', {
        method: 'POST',
        body: formData,
    });

    contentarea.style.filter = 'none';
    contentarea.style.pointerEvents = 'auto';
    spinner.style.display = 'none';

    if (!response.ok) {
        alert('Report creation failed for an unknown reason.');
        return;
    }

    const report = await response.json();
    const reportArea = document.getElementById('reportContent');
    // Convert markdown to HTML
    reportArea.innerHTML = marked.parse(report.content);
    document.getElementById('printReport').disabled = false;
});

document.getElementById('printReport').addEventListener('click', (e) => {
    var reportContent = document.getElementById('reportContent').innerHTML;

    // Create a new iframe or find the existing one.
    let printIframe = document.getElementById('printIframe');
    if (!printIframe) {
        printIframe = document.createElement('iframe');
        printIframe.id = 'printIframe';
        printIframe.style.display = 'none';
        document.body.appendChild(printIframe);
    }

    // Copy the text into the new iframe.
    const printDocument = printIframe.contentWindow.document;
    printDocument.open();
    printDocument.write('<html><head><title>Print</title>');
    printDocument.write('<style>body { white-space: pre-wrap; word-wrap: break-word; }</style>');
    printDocument.write('</head><body>');
    printDocument.write(reportContent);
    printDocument.write('</body></html>');
    printDocument.close();

    // Call the print function on the iframe.
    printIframe.contentWindow.print();
});

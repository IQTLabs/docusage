var dragArea = document.getElementById("dragDropArea");
var fileInput = document.getElementById("fileInput");

// Highlight drop area when item is dragged over it
dragArea.addEventListener("dragover", function (event) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
    dragArea.style.borderColor = "#000";
});

// Reset drop area when item is dragged out
dragArea.addEventListener("dragleave", function (event) {
    dragArea.style.borderColor = "#aaa";
});

// Handle dropped items
dragArea.addEventListener("drop", function (event) {
    event.stopPropagation();
    event.preventDefault();

    dragArea.style.borderColor = "#aaa";

    var files = event.dataTransfer.files;

    handleFiles(files);
});

// Open file selector when clicked on the drop area
dragArea.addEventListener("click", function () {
    fileInput.click();
});

// Handle files from file dialog
fileInput.addEventListener("change", function () {
    handleFiles(fileInput.files);
});

// Handle the files
function handleFiles(files) {
    console.log(files);
}

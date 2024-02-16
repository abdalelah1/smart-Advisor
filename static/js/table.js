document.getElementById("excelFileInput").addEventListener("change", function (event) {
    const fileInput = event.target;
    if (fileInput.files.length > 0) {
        const selectedFile = fileInput.files[0];
    
        alert("Selected file: " + selectedFile.name);
    }
});
console.log('table')
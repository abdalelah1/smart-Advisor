// Toggle the visibility of the course form
let addCourseFormVisible = false;
console.log('major')
document.getElementById("addCourses").addEventListener("click", () => {
    const coursesForm = document.getElementById("coursesForm");
    addCourseFormVisible = !addCourseFormVisible;
    coursesForm.style.display = addCourseFormVisible ? "block" : "none";
});




// Get references to the university form inputs
const majorNameInput = document.getElementById("majorName");


// Add an input event listener to the university form inputs
universityNameInput.addEventListener("input", toggleAddCoursesButton);
requiredCoursesInput.addEventListener("input", toggleAddCoursesButton);

// Function to toggle the "Add Courses" button based on university form completion
function toggleAddCoursesButton() {
    const addCoursesButton = document.getElementById("addCourses");
    // Check if both university form inputs have values
    if (universityNameInput.value.trim() !== "" && requiredCoursesInput.value.trim() !== "") {
        addCoursesButton.removeAttribute("disabled"); // Enable the button
    } else {
        addCoursesButton.setAttribute("disabled", "true"); // Disable the button
    }
}

// Toggle the visibility of the course form
let addCourseFormVisible = false;
console.log('college')

document.getElementById("addCourses").addEventListener("click", () => {
    const coursesForm = document.getElementById("coursesForm");
    addCourseFormVisible = !addCourseFormVisible;
    coursesForm.style.display = addCourseFormVisible ? "block" : "none";

    // Clear both input fields
   
});


document.getElementById("savecollegeInfo").addEventListener("click", () => {
    const Collegename = document.getElementById("Collegename").value;

    if (!Collegename) {
        alert("Please fill in all required fields.");
    } else {
        alert("College info saved!");

        // Clear the form inputs
        document.getElementById("Collegename").value = "";
        document.getElementById("requiredCourses").value = ""; // Add this line to clear the requiredCourses input
    }
});


document.getElementById("saveCourse").addEventListener("click", () => {
    const courseName = document.getElementById("courseName").value;
    const courseCode = document.getElementById("courseCode").value;
    const courseLevel = document.getElementById("courseLevel").value;
    const courseCredit = document.getElementById("courseCredit").value;
    const hoursCondition = document.getElementById("hoursCondition").value;

    if (!courseName || !courseCode || !courseLevel || !courseCredit || !hoursCondition) {
        alert("Please fill in all required fields.");
    } else {
        alert("Course info saved!");

        // Clear the form inputs
        document.getElementById("courseName").value = "";
        document.getElementById("courseCode").value = "";
        document.getElementById("courseLevel").value = "";
        document.getElementById("courseCredit").value = "";
        document.getElementById("hoursCondition").value = "";
        document.getElementById("requiredTrue").checked = false;
        document.getElementById("requiredFalse").checked = false;
    }
});

// Show the footer when scrolling to the end of the page
window.addEventListener("scroll", () => {
    const footer = document.getElementById("site-footer");
    const scrollHeight = document.documentElement.scrollHeight;
    const scrollPosition = window.innerHeight + window.scrollY;

    if (scrollPosition >= scrollHeight) {
        footer.style.zIndex = "1";
        footer.style.transform = "translateY(0)";
    } else {
        footer.style.zIndex = "-1";
        footer.style.transform = "translateY(100%)";
    }
});
const word1 = document.querySelector('.word1');
const word2 = document.querySelector('.word2');

let isWord1 = true;

setInterval(function () {
    if (isWord1) {
        word1.style.color = "#000d2b"; // Change the color to the second word's color
        word2.style.color = "#14a5a3"; // Change the color to the first word's color
    } else {
        word1.style.color = "#14a5a3"; // Change the color to the first word's color
        word2.style.color = "#000d2b"; // Change the color to the second word's color
    }
    isWord1 = !isWord1;
}, 2000); // Change colors every 2 seconds (adjust the timing as needed)

document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.getElementById("savecollegeInfo");
    const Collegename = document.getElementById("Collegename");
    const requiredCoursesInput = document.getElementById("requiredCourses");

    // Add a click event listener to the "Save" button
    saveButton.addEventListener("click", function () {
        console.log("Save  clicked");
        // Clear the input fields by setting their values to empty strings
        Collegename.value = "";
        requiredCoursesInput.value = "";
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // Select the "Save Course" button and the input fields in the "Course Info" form
    const saveCourseButton = document.getElementById("saveCourse");
    const courseNameInput = document.getElementById("courseName");
    const courseCodeInput = document.getElementById("courseCode");
    const courseLevelInput = document.getElementById("courseLevel");
    const courseCreditInput = document.getElementById("courseCredit");
    const requiredTrueInput = document.getElementById("requiredTrue");
    const requiredFalseInput = document.getElementById("requiredFalse");
    const hoursConditionInput = document.getElementById("hoursCondition");

    // Add a click event listener to the "Save Course" button
    saveCourseButton.addEventListener("click", function () {
        // Clear the input fields by setting their values to empty strings
        courseNameInput.value = "";
        courseCodeInput.value = "";
        courseLevelInput.value = "";
        courseCreditInput.value = "";
        requiredTrueInput.checked = false;
        requiredFalseInput.checked = false;
        hoursConditionInput.value = "";
    });
});
// Get references to the university form inputs
const Collegename = document.getElementById("Collegename");
const requiredCoursesInput = document.getElementById("requiredCourses");

// Add an input event listener to the university form inputs
Collegename.addEventListener("input", toggleAddCoursesButton);
requiredCoursesInput.addEventListener("input", toggleAddCoursesButton);

// Function to toggle the "Add Courses" button based on university form completion
function toggleAddCoursesButton() {
    const addCoursesButton = document.getElementById("addCourses");
    // Check if both university form inputs have values
    if (Collegename.value.trim() !== "" && requiredCoursesInput.value.trim() !== "") {
        addCoursesButton.removeAttribute("disabled"); // Enable the button
    } else {
        addCoursesButton.setAttribute("disabled", "true"); // Disable the button
}
}
// Toggle the visibility of the course form
let addCourseFormVisible = false;
console.log('departments')
document.getElementById("addCourses").addEventListener("click", () => {
    const coursesForm = document.getElementById("coursesForm");
    addCourseFormVisible = !addCourseFormVisible;
    coursesForm.style.display = addCourseFormVisible ? "block" : "none";

    // Clear both input fields
    const courseNameInput = document.getElementById("courseName");
    const courseCodeInput = document.getElementById("courseCode");
    const courseLevelInput = document.getElementById("courseLevel");
    const courseCreditInput = document.getElementById("courseCredit");
    const hoursConditionInput = document.getElementById("hoursCondition");

    courseNameInput.value = "";
    courseCodeInput.value = "";
    courseLevelInput.value = "";
    courseCreditInput.value = "";
    hoursConditionInput.value = "";
    document.getElementById("requiredTrue").checked = false;
    document.getElementById("requiredFalse").checked = false;
});

document.getElementById("saveDepartmentInfo").addEventListener("click", () => {
    const departmentName = document.getElementById("Departmentname").value;
    const fullCourseHours = document.getElementById("fullCourseHours").value;
    const hoursGraduated = document.getElementById("hoursGraduated").value;
    const hoursElective = document.getElementById("hoursElective").value;

    if (!departmentName || !fullCourseHours || !hoursGraduated || !hoursElective) {
        alert("Please fill in all required fields.");
    } else {
        alert("Department info saved!");

        // Clear the form inputs
        document.getElementById("Departmentname").value = "";
        document.getElementById("fullCourseHours").value = "";
        document.getElementById("hoursGraduated").value = "";
        document.getElementById("hoursElective").value = "";
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
});

document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.getElementById("saveDepartmentInfo");
    const departmentName = document.getElementById("Departmentname");
    const fullCourseHoursInput = document.getElementById("fullCourseHours");
    const hoursGraduatedInput = document.getElementById("hoursGraduated");
    const hoursElectiveInput = document.getElementById("hoursElective");

    // Add a click event listener to the "Save" button
    saveButton.addEventListener("click", function () {
        // Clear the input fields by setting their values to empty strings
        departmentName.value = "";
        fullCourseHoursInput.value = "";
        hoursGraduatedInput.value = "";
        hoursElectiveInput.value = "";
    });
});

// Get references to the department form inputs
const departmentName = document.getElementById("Departmentname");
const fullCourseHoursInput = document.getElementById("fullCourseHours");
const hoursGraduatedInput = document.getElementById("hoursGraduated");
const hoursElectiveInput = document.getElementById("hoursElective");

// Add an input event listener to the department form inputs
departmentName.addEventListener("input", toggleAddCoursesButton);
fullCourseHoursInput.addEventListener("input", toggleAddCoursesButton);
hoursGraduatedInput.addEventListener("input", toggleAddCoursesButton);
hoursElectiveInput.addEventListener("input", toggleAddCoursesButton);

// Function to toggle the "Add Courses" button based on department form completion
function toggleAddCoursesButton() {
    const addCoursesButton = document.getElementById("addCourses");
    // Check if all department form inputs have values
    if (
        departmentName.value.trim() !== "" &&
        fullCourseHoursInput.value.trim() !== "" &&
        hoursGraduatedInput.value.trim() !== "" &&
        hoursElectiveInput.value.trim() !== ""
    ) {
        addCoursesButton.removeAttribute("disabled"); // Enable the button
    } else {
        addCoursesButton.setAttribute("disabled", "true"); // Disable the button
    }
}

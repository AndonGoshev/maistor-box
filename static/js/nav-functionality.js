// document.addEventListener("DOMContentLoaded", () => {
//     const menuToggle = document.getElementById("menu-toggle");
//     const menuIcon = document.querySelector(".menu-icon");
//     const dropdownMenu = document.querySelector(".dropdown-menu");
//
//     // Toggle menu on icon click
//     menuIcon.addEventListener("click", () => {
//         menuToggle.checked = !menuToggle.checked; // Toggle the checkbox
//     });
//
//     // Close the dropdown menu when clicking outside
//     document.addEventListener("click", (event) => {
//         if (!menuIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
//             menuToggle.checked = false; // Hide the menu
//         }
//     });
// });
// main.js
document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const registrationForm = document.getElementById("registrationForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            // Handle login form submission
            // You can use Fetch API to send data to your backend
        });
    }

    if (registrationForm) {
        registrationForm.addEventListener("submit", function(event) {
            event.preventDefault();
            // Handle registration form submission
            // You can use Fetch API to send data to your backend
        });
    }
});
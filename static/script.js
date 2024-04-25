// script.js
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("registerForm").addEventListener("submit", function(event) {
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!isValidEmail(email)) {
            alert("Please enter a valid email address.");
            event.preventDefault();
        }
    });
});

function isValidEmail(email) {
    // Simple email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("loginForm").addEventListener("submit", function(event) {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        if (!isValidUsername(username)) {
            alert("Please enter a valid username/email.");
            event.preventDefault();
        }
    });
});

function isValidUsername(username) {
    // Simple username/email validation regex
    const usernameRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return usernameRegex.test(username);
}


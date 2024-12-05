const loginForm = document.getElementById("login-form");
const loginButton = document.getElementsByClassName("submit-button");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton[0].addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "osama" && password === "SmartSpace") {
        alert("You have successfully logged in.");
        location.reload();
        loginErrorMsg.style.opacity = 0;
        window.location.href = "finalproject.html"
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})

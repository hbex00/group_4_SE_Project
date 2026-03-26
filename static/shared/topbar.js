const logo = document.querySelector(".logo");

logo.addEventListener("click", () => {
    window.location.href = "../homepage/homepage.html";
});

const user_icon = document.getElementById("user_icon");

user_icon.addEventListener("click", () => {
    window.location.href = "../loginpage/loginpage.html";
});

/* logo is a div*/
const logo = document.getElementById("logo");

const form = document.querySelector("form");

logo.addEventListener("click", () => {
    form.submit();
});


const user_icon = document.getElementById("user_icon");

const user = document.getElementById("user");

user_icon.addEventListener("click", () => {
    user.submit();
});
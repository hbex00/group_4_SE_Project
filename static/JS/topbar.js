
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


const profile_button = document.getElementById("profile_button");

const profile_form = document.getElementById("profile");

profile_button.addEventListener("click", () => {
    profile_form.submit();
});


const recipe_button = document.getElementById("recipe_button");

const recipe_form = document.getElementById("recipe");

recipe_button.addEventListener("click", () => {
    recipe_form.submit();
});


const logout_button = document.getElementById("logout_button");

const logout_form = document.getElementById("logout");

logout_button.addEventListener("click", () => {
    logout_form.submit();
});
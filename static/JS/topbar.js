
/* logo is a div*/
const logo = document.getElementById("logo");

const form = document.querySelector("form");

logo.addEventListener("click", () => {
    form.submit();
});
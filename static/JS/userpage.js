
document.addEventListener("DOMContentLoaded", () => {
    const recipe_card_list = document.querySelectorAll(".recipe_card");

    recipe_card_list.forEach(div => {
        div.addEventListener("click", () => {
            div.querySelector("form").submit();
        });
    });
});

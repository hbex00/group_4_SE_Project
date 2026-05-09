const recipe_card_list = document.querySelectorAll(".recipe_card");
const toggle_button = document.querySelector(".filter_toggle");
const filter_menu = document.querySelector(".filter_menu");

toggle_button.addEventListener('click', () => {
    filter_menu.style.display = filter_menu.style.display === 'block' ? 'none' : 'block'
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.filter_dropdown')) {
        filter_menu.style.display = 'none';
    }
});

recipe_card_list.forEach(div => {
    div.addEventListener("click", () => {
        div.querySelector("form").submit();
    });
});
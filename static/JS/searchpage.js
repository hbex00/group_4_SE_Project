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

document.addEventListener("DOMContentLoaded", () => {
    const type_checkboxes = document.querySelectorAll(".type_checkbox");

    function update_filters() {
        type_checkboxes.forEach(checkbox => {
            const target_ID = checkbox.dataset.target;
            const target = document.getElementById(target_ID);

            if (!target){
                return;
            }
            if (checkbox.checked) {
                target.style.display = "flex";
            }
            else{
                target.style.display = "none";
            }
        });
    }
    type_checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change",update_filters)
    })
    update_filters();
})

recipe_card_list.forEach(div => {
    div.addEventListener("click", () => {
        div.querySelector("form").submit();
    });
});
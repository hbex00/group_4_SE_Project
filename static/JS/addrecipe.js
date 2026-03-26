

const add_ingredient_btn = document.getElementById("ingredient_btn");

const ingredient_div_location = document.querySelector(".tmp");

add_ingredient_btn.addEventListener("click", () => {
    const new_div = document.createElement("div");
    new_div.className = "ingredient_div";
    
    const new_ingredient_input_box = document.createElement("input");
    new_ingredient_input_box.type = "input";
    new_ingredient_input_box.placeholder = "Ingredient name";
    new_ingredient_input_box.size = 50;
    new_div.appendChild(new_ingredient_input_box);

    const new_amount_input_box = document.createElement("input");
    new_amount_input_box.placeholder = "Amount";
    new_amount_input_box.size = 5;
    new_div.appendChild(new_amount_input_box);

    const new_unit_input_box = document.createElement("input");
    new_unit_input_box.placeholder = "unit";
    new_unit_input_box.size = 10;
    new_div.appendChild(new_unit_input_box);

    ingredient_div_location.appendChild(new_div);
});
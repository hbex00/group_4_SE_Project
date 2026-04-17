const add_step_btn = document.getElementById("step_btn");

const step_div_location = document.querySelector(".step");

let j = 0;

add_step_btn.addEventListener("click", () => {
    if (j < 20) {
        const new_div = document.createElement("div");
        new_div.className = "ingredient_div";

        const new_step = document.createElement("input");
        new_step.name = "step[]";
        new_step.placeholder = `Step ${j + 1}`;
        new_step.size = 40;
        new_div.appendChild(new_step);

        const new_delete_btn = document.createElement("p");
        new_delete_btn.innerHTML ="&minus;";
        new_delete_btn.style = "-webkit-user-select: none; user-select: none;";
        new_div.appendChild(new_delete_btn);

        new_delete_btn.addEventListener("click", () => {
            new_div.remove();
            j--;
        });

        step_div_location.appendChild(new_div);
        j++;
    }
});

const add_ingredient_btn = document.getElementById("ingredient_btn");

const ingredient_div_location = document.querySelector(".ingredient");

let i = 0;

add_ingredient_btn.addEventListener("click", () => {
    if (i < 20) {
        const new_div = document.createElement("div");
        new_div.className = "ingredient_div";
        
        const new_ingredient_input_box = document.createElement("input");
        new_ingredient_input_box.type = "input";
        new_ingredient_input_box.placeholder = `Ingredient ${i + 1}`;
        new_ingredient_input_box.size = 50;
        new_ingredient_input_box.name = "ingredients[]";
        new_div.appendChild(new_ingredient_input_box);

        const new_amount_input_box = document.createElement("input");
        new_amount_input_box.placeholder = "Amount";
        new_amount_input_box.size = 5;
        new_amount_input_box.name = "amount[]";
        new_div.appendChild(new_amount_input_box);

        const new_unit_input_box = document.createElement("input");
        new_unit_input_box.placeholder = "unit";
        new_unit_input_box.size = 10;
        new_unit_input_box.name = "unit[]";
        new_div.appendChild(new_unit_input_box);


        const new_delete_btn = document.createElement("p");
        new_delete_btn.innerHTML ="&minus;";
        new_delete_btn.style = "-webkit-user-select: none; user-select: none;";
        new_div.appendChild(new_delete_btn);

        new_delete_btn.addEventListener("click", () => {
            new_div.remove();
            i--;
        });

        ingredient_div_location.appendChild(new_div);
        i++;
    }
});


const min  = document.getElementById("minus");
const plus = document.getElementById("plus");
const portion = document.getElementById("portions");

min.addEventListener("click", () => {
    let value = portion.valueAsNumber;
    if (value > portion.min) {
        portion.value = value - 1;
    }
});
plus.addEventListener("click", () => {
    let value = portion.valueAsNumber;
    if (value < portion.max) {
        portion.value = value + 1;
    }
});
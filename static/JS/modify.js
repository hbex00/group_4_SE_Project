
/* ----------------------------------------------
 * Portions JS
 * ----------------------------------------------
 */
const minus = document.getElementById("minus");
const plus = document.getElementById("plus");
const portions = document.getElementById("portions");

/* Decreasing the amount of portions by one, downto 1
*/
minus.addEventListener("click", () => {
    let val = portions.valueAsNumber;
    if (val > portions.min) {
        portions.value = val - 1;
    }
});
/* Ingreasing the amount of portions by one, up to max 16
*/
plus.addEventListener("click", () => {
    let val = portions.valueAsNumber;
    if (val < portions.max) {
        portions.value = val + 1;
    }
});


/* ----------------------------------------------
 * Ingredients JS
 * ----------------------------------------------
 */
const ingredient_location = document.getElementById("ingredient_location");

/* Remove a ingredient, including the amount and unit
 * This is for the ingreadints that come with the old recipe
*/
const minus_ingr = document.querySelectorAll(".minus_ingredient");
minus_ingr.forEach(button => {
    button.addEventListener("click", () => {
        button.parentElement.remove();
    });
});

/* Button to add ingredient, also adds amount, unit and remove btn
*/
const btn = document.getElementById("add_ingr_btn");

let i = document.querySelectorAll(".ingredient_div").length;

btn.addEventListener("click", () => {
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

        ingredient_location.appendChild(new_div);
        i++;
    }
});



/* ----------------------------------------------
 * Steps JS
 * ----------------------------------------------
 */
const add_step_btn = document.getElementById("add_step_btn");
const step_div_location = document.getElementById("step_location");

let j = document.querySelectorAll(".steps").length;;
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


/* Remove a step
 * This is for the steps that come with the old recipe
*/
const minus_step = document.querySelectorAll(".minus_step");
minus_step.forEach(button => {
    button.addEventListener("click", () => {
        button.parentElement.remove();
    });
});

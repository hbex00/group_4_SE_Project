// Getting all the categories
const tag_cat_list = document.querySelectorAll(".dropdown");

tag_cat_list.forEach(btn => {
    // finding the inputs
    let txt = btn.querySelector("input");
    let actual = btn.querySelector('input[type="hidden"]');

    // text string
    let cat = btn.querySelector("input").placeholder;

    // Getting the list of tags inside that category
    const cat_specific_table = btn.querySelectorAll("li");

    // On click changing the input to the li item clicked 
    cat_specific_table.forEach(li_element => {
        li_element.addEventListener("click", () => {
            const string = cat + ": " +li_element.innerText;
            txt.value = string;
            actual.value = string;
        });
    });

    const cat_specific_x = btn.querySelectorAll("p");

    cat_specific_x.forEach(x_element => {
        x_element.addEventListener("click", () => {
            txt.value = cat;
            actual.value = cat;
        });
    })
});
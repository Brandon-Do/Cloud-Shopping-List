"use strict";
const TARGET = document.getElementById('grocery-list');
const INPUT_NAMES = ['item-name', 'item-quantity', 'item-notes'];

let add_grocery_item_forms = (num) => {
    const input_html = "<form class='grocery-item'><input placeholder='Item Name' type='text' name='item-name'><input placeholder='Quantity' type='text' name='item-quantity'><input placeholder='Other Notes' type='text' name='item-notes'></form>";
    TARGET.innerHTML += input_html.repeat(num);
}

let get_forms = (div_id="grocery-list", form_id=".grocery-item") => {
  return [].slice.call(document.getElementById(div_id).querySelectorAll(form_id));
}

// Clear Inputs from List collection of functions:

let clear_input_values = () => {
  let grocery_forms = get_forms();
  grocery_forms
  .map(get_children) // Gets inputs from form
  .map(clear_inputs) // For each list of inputs, clear inputs
}

let get_children = (form) => {
  return [].slice.call(form.childNodes); // Returns list of inputs from form
}

let clear_inputs = (inputs) => {
  inputs.forEach(input => input.value = '')
}

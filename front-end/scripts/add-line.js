
// Add Line Items to List

const target = document.getElementById('grocery-list');
const input_names = ['item-name', 'item-quantity', 'item-notes'];

let add_line = () => {
  target.innerHTML += "<form class='grocery-item'><input type='text' name='item-name'><input type='text' name='item-quantity'><input type='text' name='item-notes'></form>"
}

let default_line_items = 5;
for (let i = 0; i<default_line_items; i++){
  add_line();
}

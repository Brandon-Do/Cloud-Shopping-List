
const target = document.getElementById('grocery-list');
const input_names = ['item-name', 'item-quantity', 'item-notes'];

let add_grocery_item_forms = (num) => {
  let input_html = "<form class='grocery-item'><input type='text' name='item-name'><input type='text' name='item-quantity'><input type='text' name='item-notes'></form>";
  target.innerHTML += input_html.repeat(num);
}

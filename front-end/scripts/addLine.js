
const target = document.getElementById('grocery-list');
const input_names = ['item-name', 'item-quantity', 'item-notes'];

let add_grocery_item_forms = (num) => {
    const input_html = "<form class='grocery-item'><input placeholder='Item Name' type='text' name='item-name'><input placeholder='Quantity' type='text' name='item-quantity'><input placeholder='Other Notes' type='text' name='item-notes'></form>";
    target.innerHTML += input_html.repeat(num);
}


// Sending JSON to AWS S3 & Dynamo DB

let send_json_grocery_list_to_s3 = () => {
  let json_grocery_list = create_grocery_list_json();
  console.log('sending JSON list....', json_grocery_list);
  send_grocery_list_to_s3(json_grocery_list);
}

let create_grocery_list_json = () => {
  let json_object = {};
  let items = get_json_list_items();
  json_object['items'] = items;
  json_object['list-name'] = document.getElementById('list-name').value;
  json_object['username'] = document.getElementById('username').value;
  return json_object;
}

let get_json_list_items = () => {
  let line_items = [].slice.call(document.getElementById("grocery-list").querySelectorAll(".grocery-item"));
  result = line_items
    .map(item => line_item_to_json(item))
    .filter(item => item['item-name'] != '');
  return result;
}

let line_item_to_json = (line_item) => {
  let json_object = {};
  for (let i = 0; i<line_item.length; i++){
    input_field = line_item[i];
    json_object[input_field.getAttribute('name')] = input_field.value;
  }
  return json_object;
}

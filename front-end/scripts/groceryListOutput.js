// Sending JSON to AWS S3 & Dynamo DB

let send_json_grocery_list_to_s3 = () => {
  let json_grocery_list = create_grocery_list_json();
  console.log('sending JSON list....', json_grocery_list);
  res = send_grocery_list_to_s3(json_grocery_list);
}

let create_grocery_list_json = () => {
  let json_object = {};
  let items = get_json_list_items();
  json_object['items'] = items;
  json_object['list-name'] = document.getElementById('list-name').value;
  json_object['username'] = document.getElementById('username').value;
  return json_object;
}

// Gets Entries from Grocery List Inputs

let get_json_list_items = () => {
  let forms = get_forms();
  result = forms
    .map(item => line_item_to_json(item))
    .filter(item => item['item-name'] != '');
  return result;
}

// Fills Entries with JSON Input

let fill_json_list_items = (json_item) => {
  let forms = get_forms();
  if (forms.length < json_item.length) {
    add_grocery_item_forms(json_item.length - forms.length);
  }
  for (let i=0; i<json_item.length; i++){
    let form = forms[i];
    let json = json_item[i];
    fill_form_with_json(form, json);
  }
}

// Helper Functions

let fill_form_with_json = (form, json) => {
  const input_names = ['item-name', 'item-quantity', 'item-notes'];
  input_names.forEach(key => {
    form[key].value = json[key];
    console.log(form[key], json[key]);
  })
}

let line_item_to_json = (line_item) => {
  let json_object = {};
  for (let i = 0; i<line_item.length; i++){
    input_field = line_item[i];
    json_object[input_field.getAttribute('name')] = input_field.value;
  }
  return json_object;
}

let get_forms = (div_id="grocery-list", form_id=".grocery-item") => {
  return [].slice.call(document.getElementById(div_id).querySelectorAll(form_id));
}

// Add Line Items to List SAFELY

let add_grocery_line = (num=1) => {
  let json_items = get_json_list_items();
  add_grocery_item_forms(num);
  fill_json_list_items(json_items);
}
add_grocery_line();

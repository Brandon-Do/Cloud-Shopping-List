"use strict";
// Created Get Shopping List Content, Add List Location as Argument,
// The API Will return GroceryListJSON, then we use populate JSON Functions
const DATA_API_URL = "https://tggnqn2byg.execute-api.us-west-2.amazonaws.com/prod/grocery-data";
const LIST_NAME_OUTPUT = document.getElementById('list-name');

let get_list_from_s3 = list_location => {
  let location_json = JSON.stringify({
    "list-location": list_location
  });
  $.post(DATA_API_URL, location_json, response => {
    let result = response['body'];
    clear_input_values();                   // clear previous list
    fill_list_name(result['list-name']);    // list-name is string
    fill_json_list_items(result['items']);  // items is an array of strings
    display_server_response(result);
  });
}

let fill_list_name = list_name => {
  LIST_NAME_OUTPUT.value = list_name;
}

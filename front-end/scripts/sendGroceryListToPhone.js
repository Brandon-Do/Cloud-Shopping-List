"use strict";
// We want to use these functions to send grocery shopping list
//  to the mobile phone using AWS-SNS

const PHONE_NUMBER_INPUT = document.getElementById("contact");
const CONTACT_API_URL = "https://tggnqn2byg.execute-api.us-west-2.amazonaws.com/prod/contact";

let send_current_list_to_phone = () => {
  let phone_number = PHONE_NUMBER_INPUT.value;
  let json_grocery_list = create_grocery_list_json();
  json_grocery_list['phone-number'] = phone_number;
  json_grocery_list = JSON.stringify(json_grocery_list);
  $.post(CONTACT_API_URL, json_grocery_list, response => {
    display_server_response(response);
  })
}

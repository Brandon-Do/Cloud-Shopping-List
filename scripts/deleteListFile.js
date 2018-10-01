"use strict";
// This will communicate with the grocery-lists resource
//  using http DELETE to remove grocery lists from DynamoDB

// delete target shopping list
let delete_list = (delete_all=false) => {
  const username = USERNAME_INPUT.value;
  const list_name = LIST_NAME_OUTPUT.value;
  const request = JSON.stringify({
    "username": username,
    "list-name": list_name,
    "delete-all": delete_all // Will check for this on server-side
  });
  $.delete(API_URL, request, response => {
    console.log(response);
    display_server_response(response);
  })
}

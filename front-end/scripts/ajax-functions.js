
// Establishing connection to API Gateway GroceryListAPI

const API_URL = "https://tggnqn2byg.execute-api.us-west-2.amazonaws.com/prod/grocery-lists";

let ajax_request = (url, data, callback, method) => {
  return $.ajax({
    url: url,
    type: method,
    crossDomain: true,
    data: data,
    // headers: {
    // // Token Here
    // },
    dataType: 'json',
    contentType: 'application/json',
    success: callback
  });
}

jQuery.extend({
    get: (url, data, callback) => {
      return ajax_request(url, data, callback, 'GET');
    },
    post: (url, data, callback) => {
        return ajax_request(url, data, callback, 'POST');
    }
});

// Invoke GroceryListAPI PUT

let send_grocery_list_to_s3 = (grocery_list_json) => {
  console.log('in send grocery list');
  grocery_list_json = JSON.stringify(grocery_list_json);
  console.log('grocery_list_json',grocery_list_json);
  $.post(API_URL, grocery_list_json, (response) => {
    console.log('response: ', response);
  })
}

// Invoke GroceryListAPI GET

let invoke_get = () => {
  $.get(API_URL, {"message":"Hello Lambda"}, (response) => {
    console.log('successfully called API Gateway');
    console.log(response['body']);
  });
}


const SEARCH_API_URL = "https://tggnqn2byg.execute-api.us-west-2.amazonaws.com/prod/search";
const SEARCH_INPUT = document.getElementById("groceryListSearchInput");
const SEARCH_OUTPUT = document.getElementById("groceryListSearchOutput");
const USERNAME_INPUT = document.getElementById('username');
const LIMIT_DEFAULT = "10";
const SEARCH_KEY_DEFAULT = "date-created";

let searchGroceryLists = () => {
  let search_query = SEARCH_INPUT.value;
  let username = USERNAME_INPUT.value;
  let search_json = JSON.stringify({
    "username": username,
    "list-name": search_query,
    "limit": LIMIT_DEFAULT,
    "sort-key": SEARCH_KEY_DEFAULT
  });
  $.post(SEARCH_API_URL, search_json, (response) => {
    console.log("Database items that match: ", search_query);
    display_search_results(response['body']);
  });
}

// Displays Search Results to user
let display_search_results = items => {
  $("#groceryListSearchOutput").empty(); // clear previous search results
  items.forEach(item => {
    item = JSON.parse(item);
    let list_attributes = ['list-name', 'date-created'];
    create_list_item(item, list_attributes);
  })
}

let create_list_item = (item, list_attributes) => {
  let onclick_function = "on_click_function('"+item['list-name']+ "');";
  console.log(onclick_function);
  let list_item = $('<li/>')
    .addClass('search-result-list-item')
    .attr('onclick', onclick_function)
    .appendTo(SEARCH_OUTPUT);
  list_attributes.forEach(attr => {
    let display_text = item[attr];
    let span_item = $('<span/>')
      .text(display_text)
      .addClass(attr)
      .appendTo(list_item);
  });
}

let on_click_function = (text) => {console.log(text)};

// To Do
// Create Get Shopping List Content, Add List Location as Argument,
// The API Will return GroceryListJSON, then we use populate JSON Functions

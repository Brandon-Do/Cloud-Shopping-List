
// Communicating with AWS API Gateway & Lambda Functions

let get_api_response = () => {
  const API_URL = "https://tggnqn2byg.execute-api.us-west-2.amazonaws.com/prod/grocery-lists";
  $.ajax({
    type: 'GET',
    url: API_URL,

    success: (response) => {
      console.log('successfully called API Gateway');
      console.log(response['body']);
    }
  })
}

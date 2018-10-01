# Cloud Shopping List

This web app was designed using a serverless architecture, built to be highly scaleable! The code is executed on demand, there are no servers hosting a running application.
This is done using AWS Lambda, triggering Lambda functions through API Gateway. This web app has been built on-top of AWS resources such as Lambda and API Gateway, DynamoDB, S3, and SNS (also utilized IAM for roles/permissions).

[LINK TO PROJECT](http://cloudshoppinglist.com.s3-website-us-east-1.amazonaws.com/)
## What does this Application Do?

The web application in concept is simple! Users are able to input their username and create grocery lists. The grocery lists are tied to the username and can be saved to the database. The grocery list can be sent to a phone number by text message!

When a grocery list is stored, the data itself is transformed into a string and stored onto a text document in S3. The meta-data, which includes the location of the text file, the name, and the user who stored it, is stored onto DynamoDB. Storing the text onto S3 allows me to get the fast reads of DynamoDB while avoiding exceeding the 400Kb memory limit of DynamoDB.

When a list is saved or deleted, both the corresponding S3 bucket and DynamoDB table are updated using Lambda functions.

>Future Additions
>Add security features using STS

## Technologies That Will Be Used

Front-End:
- JavaScript
- jQuery, AJAX

Back-End:
- AWS Lambda (Python)
- AWS API Gateway
- AWS S3
- AWS DynamoDB
- AWS SNS

## Development Pictures

(10/1) Finished Project with Added Functionality:

![Project Snapshot 10/1](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list_final.PNG)

(9/25) Updated Front-End:

![Project Snapshot 9/25](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list.PNG)


(9/25) Updated DynamoDB Schema:

![Project Snapshot 9/25](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list_db_schema.PNG)


(9/12) Example of running the Lambda function through API Gateway to Store the Grocery List Data into an S3 Bucket:

![Project Snapshot 9/12](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list_stage1.PNG)


This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

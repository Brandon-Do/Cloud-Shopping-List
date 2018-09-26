# Cloud Shopping List

This web application is designed to be running serverless. This means that code is executed on demand, and that there are no running servers.
This is done using AWS Lambda, triggering Lambda functions through API Gateway. This web app will be built on-top of AWS resources such as S3, Lambda, DynamoDB, and SNS.

[LINK TO PROJECT](http://cloudshoppinglist.com.s3-website-us-east-1.amazonaws.com/)

> Please note: this project is under construction as of 9/25/2018

## What does this Application Do?

The web application in concept is simple! I plan on letting users create shopping lists using the web application and then sending them 
the lists using email and phone. The users will be able to create their accounts, where the lists will be binded to their account.
The lists will be stored onto an S3 bucket, and the list meta-data will be stored onto DynamoDB for fast reads! 

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

(9/25) Updated Front-End:

![Project Snapshot 9/25](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list.PNG)


(9/25) Updated DynamoDB Schema:

![Project Snapshot 9/25](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list_db_schema.PNG)


(9/12) Example of running the Lambda function through API Gateway to Store the Grocery List Data into an S3 Bucket:

![Project Snapshot 9/12](https://s3-us-west-2.amazonaws.com/brandon-do-public/portfolio/cloud-shopping-list/cloud_shopping_list_stage1.PNG)


This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

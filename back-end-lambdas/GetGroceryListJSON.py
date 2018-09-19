import boto3
import botocore
import json
import os

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    """Gets meta-data from DynamoDB of grocery LISTS

    """
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }

def getGroceryListLocation(username, listname):
    """ Fetch list meta data from DynamoDB

    username -- The username of the account fetching the list
    listname -- the name of the grocery list in the DB
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    pass
    # response = table.query(
    #     KeyConditionExpression=Key('username').eq(event['username'])
    # )

def convertTextFiletoGroceryListJson(location):
    """Get txt file from S3

    location -- the location of the file
    """
    pass # Implement

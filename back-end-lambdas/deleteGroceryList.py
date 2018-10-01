import os
import botocore
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Global variables used by all functions
REGION = os.environ['REGION']
BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
s3 = boto3.resource('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """Deletes database items based on the front-end request.
    """
    username = event['username']
    list_name = event['list-name']
    delete_all = event['delete-all'] # boolean
    list_location = generateListLocation(username, list_name)

    if delete_all:
        deleteDBRange(username)
        return {"statusCode": 200, "message": "All lists associated with {} have been deleted!".format(username) }

    if not fileExistsInBucket(list_location, BUCKET_NAME):
        return {"statusCode": 200, "message": "{} had never existed in the first place.".format(list_name) + list_location}

    deleteDBItem(username, list_location)
    return {"statusCode": 200, "message": "Removed {} from our database.".format(list_name)}

##########################
### DynamoDB Functions ###
##########################

def deleteDBItem(partition_key, sort_key):
    """ Deletes a row off the DynamoDB table using associated key

    Keyword Arguments
    partition_key -- username
    sort_key -- the list's location, output of generateListLocation
    """
    table.delete_item(
        Key = {
            "username":partition_key,
            "list-location":sort_key
        }
    )

def deleteDBRange(username):
    """ Get all db items within a range using partition_key and sort_key,
        then delete them all.

        In this case we want to delete all db items associate with a username
        We query the table using the partition key and then delete all resulting items.

    Keyword Arguments
    username -- The username of the account fetching the list
    """
    ce = Key('username').eq(username)
    response = table.query(
        KeyConditionExpression = ce
    )
    items = response["Items"]
    for item in items:
        list_location = item['list-location']
        deleteDBItem(username, list_location)

########################
### Helper Functions ###
########################

def generateListLocation(username, list_name):
    """ generates file placement in S3 based on standardized storage 
    """
    return username + '/' + list_name + '.txt'

def fileExistsInBucket(file_name, bucket_name):
    """ Checks if the name of text_file is already taken in the bucket

    Keyword Arguments:
    file_name -- Output of generateTextFileName
    bucket_name -- Name of environment variable for S3 bucket
    """
    file_exists = False

    try:
        s3.Object(bucket_name, file_name).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return file_exists
    else:
        file_exists = True
    return file_exists

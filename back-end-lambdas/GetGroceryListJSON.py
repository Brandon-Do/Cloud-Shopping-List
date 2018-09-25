import os
import botocore
import boto3
import json
from datetime import datetime


# Global variables used by all functions
REGION = os.environ['REGION']
BUCKET_NAME = os.environ['BUCKET_NAME']
s3 = boto3.resource('s3', region_name=REGION)

def lambda_handler(event, context):
    """Gets meta-data from DynamoDB of grocery LISTS

    """
    try:
        list_location = event['list-location']
        text_data = getTextFileData(list_location)
        if not text_data:
            return {
            "statusCode": 404,
            "body": "File does not exist"
            }
        grocery_list_json = groceryListTextToJson(text_data)

        return {
            "statusCode": 200,
            "body": grocery_list_json
        }
    except:
        return {
            "statusCode": 400,
            "body": "serverside error"
        }

def groceryListTextToJson(text_data):
    """ converts grocery list string to grocery list json

    Keyword Arguments
    text -- text data stored on s3 using JSONtoS3 lambda function
    """
    list_json = json.loads(text_data)
    list_json['message'] = 'Loaded the saved list: ' + list_json['list-name']
    return list_json

def getTextFileData(list_location):
    """Using list location, get text data from that location

    Keyword Arguments
    location -- the location of the file
    """
    try:
        s3.Object(BUCKET_NAME, list_location).load() # check if the item exists first
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print('the item does not exist')
            return ''
        else:
            raise
    else:
        f = s3.Object(BUCKET_NAME, list_location)       # get s3 file object
        text = f.get()['Body'].read().decode('utf-8')   # get text file data from object
        return text

def BucketExists():
    """ Checks if the bucket DOESN'T exist

    Keyword Arguments:
    s3 -- s3 resource object
    bucket_name -- the bucket name
    """
    bucket = s3.Bucket(bucket_name)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
    return exists

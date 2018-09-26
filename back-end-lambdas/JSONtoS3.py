import os
import botocore
import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    """ Takes grocery list JSON, stores meta-data in DynamoDB and list in S3

    Keyword Arguments
    event -- JSON Grocery List with user-data
    context -- Request headers
    """
    try:
        file_name = generateTextFileName(event)
        if textFileExistsInBucket(file_name, os.environ['BUCKET_NAME']):
            return {
                "message":"Error, List Name exists! Delete the old list before creating the new one.",
                "status_code":"418"
            }

        putJSONListIntoBucket(event, file_name)     # Store grocery list 'items' to txt file on S3, return
        storeMetaDataOnDynamo(event, file_name)     # Attach name of file
                                                    # Note to Self, update list view with new lambda function after this has been stored.
        return {'message':'{} Saved!'.format(event['list-name']), 'status_code':200 }
    except:
        return {'message':"Serverside error", 'status_code':400}

###########################
### Dynamo DB Functions ###
###########################

def storeMetaDataOnDynamo(event, text_file_name)   :
    """ Take JSON and name of text file stored on S3, put onto Dynamo Table

    Keyword Arguments
    event -- JSON grocery list
    text_file_name -- Name of txt file of JSON stored onto S3
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    current_time = datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    json_item = {
            'username': event['username'],
            'list-location': text_file_name,
            'date-created': current_time,
            'list-name': event['list-name'],
        } # Item to be store in DynamoDB
    table.put_item(Item=json_item)

###########################
### S3 Bucket Functions ###
###########################

def textFileExistsInBucket(file_name, bucket_name):
    """ Checks if the name of text_file is already taken in the bucket

    Keyword Arguments:
    file_name -- Output of generateTextFileName
    bucket_name -- Name of environment variable for S3 bucket
    """
    s3 = boto3.resource('s3')
    bucket_name =  os.environ['BUCKET_NAME']
    file_exists = False

    try:
        s3.Object(bucket_name, file_name).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return file_exists
    else:
        file_exists = True
    return file_exists

def putJSONListIntoBucket(event, file_name):
    """ Stores JSON Items as text file in S3

    Keyword Arguments
    event -- JSON grocery list
    """
    s3 = boto3.resource('s3')
    bucket_name =  os.environ['BUCKET_NAME']

    if doesBucketNotExist(s3, bucket_name):
        print("Creating bucket: ", bucket_name)
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
    'LocationConstraint': 'us-west-2'})

    text_data = json.dumps(event)
    lambda_path = "/tmp/" + file_name
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=text_data.encode("utf-8"))
    return file_name # Return file_name to be stored into dyanmo

def doesBucketNotExist(s3, bucket_name):
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

    return not exists

###################################
### Formatting Helper Functions ###
###################################

def generateTextFileName(event):
    """ Generates file name for txt grocery list to store on S3

    Keyword Arguments
    event -- JSON grocery list
    """
    return event['username'] + '/' + event['list-name'] + '.txt'

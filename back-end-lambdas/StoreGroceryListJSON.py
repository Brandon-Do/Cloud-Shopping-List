import os
import botocore
import boto3
import datetime

from random import randint

def lambda_handler(event, context):
#try:
    file_name = generateTextFileName(event)
    if textFileExistsInBucket(file_name, os.environ['BUCKET_NAME']):
        return {
            "message":"Error, List Name exists! Delete the old list before creating the new one.",
            "status_code":"418"
        }
    putJSONListIntoBucket(event, file_name)     # Store grocery list 'items' to txt file on S3, return
    storeMetaDataOnDynamo(event, file_name)     # Attach name of file
    # Note to Self, update list view with new lambda function after this has been stored.
    return {'message':'{} Saved!'.format(event['list-name']), 'status_code':200}
#except:
    return {'message':"Serverside error", 'status_code':300}

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
    partition_key = generatePartitionDateKey()
    json_item = {
            'partition-date': partition_key,
            'username': event['username'],
            'list-name': event['list-name'],
            'list-location': text_file_name
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

    # Implement Me
    return False

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

    text_data = createTextDataFromJSON(event['list-name'], event['items'])
    lambda_path = "/tmp/" + file_name
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=text_data.encode("utf-8"))
    return file_name # Return file_name to be stored into dyanmo

def createTextDataFromJSON(list_name, items):
    """ Takes list-name and list items from JSON, converts to string

    Keyword Arguments
    list_name -- The name of the list
    items -- A list of grocery list JSON items
    """
    text_data = list_name + '\n'
    for item in items:
        text_data += str(item) + '\n'
    return text_data

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

def generatePartitionDateKey(date_format='%Y-%m-%d'):
    """ Generate date-based partition key, spread across ten partitions 0-9

    Keyword Arguments
    date_format -- date format for strftime "string format time"
    """
    now = datetime.datetime.now()
    partition_number = str(randint(0, 9))
    return partition_number + '-' + now.strftime(date_format)

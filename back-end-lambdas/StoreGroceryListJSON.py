import os
import botocore
import boto3

def lambda_handler(event, context):
    #try:
    text_file_name = putJSONListIntoBucket(event)   # Store grocery list 'items' to txt file on S3, return
    storeMetaDataOnDynamo(event, text_file_name)    # Attach name of file
    return {'message':'{} Saved!'.format(event['list-name']), 'status_code':200}
    #except:
    #    return {'message':"Serverside error", 'status_code':300}

def storeMetaDataOnDynamo(event, text_file_name)   :
    """ Take JSON and name of text file stored on S3, put onto Dynamo Table

    Keyword Arguments
    event -- JSON grocery list
    text_file_name -- Name of txt file of JSON stored onto S3
    """
    pass

def putJSONListIntoBucket(event):
    """ Stores JSON Items as text file in S3

    Keyword Arguments
    event -- JSON grocery list
    """
    s3 = boto3.resource('s3')
    bucket_name = os.environ['BUCKET_NAME']

    if doesBucketNotExist(s3, bucket_name):
        print("Creating bucket: ", bucket_name)
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
    'LocationConstraint': 'us-west-2'})

    text_data = createTextDataFromJSON(event['list-name'], event['items'])
    file_name = event['list-name'] + '.txt' # Note, implement check if overwriting existing list
    lambda_path = "/tmp/" + file_name
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=text_data.encode("utf-8"))

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

import os
import botocore
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket_name = os.environ['BUCKET_NAME']
    
    try:
        if doesBucketNotExist(s3, bucket_name):
            print("Creating bucket: ", bucket_name)
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})
    
        text_data = event['list-name'] + '\n'
        for item in event['items']:
            text_data += str(item) + '\n'
        
        file_name = event['list-name'] + '.txt' # Note, implement check if overwriting existing list
        lambda_path = "/tmp/" + file_name
        
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=text_data.encode("utf-8"))
     
        return event
    except:
        return {'message':"Serverside error", 'status_code':300}

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

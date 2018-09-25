import boto3
import botocore
import decimal
import json
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Global variables used by all functions
TABLE_NAME = os.environ['TABLE_NAME']
REGION = os.environ['REGION']
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """Gets meta-data from DynamoDB of grocery lists, returns matching results
    """
    try:
        listname = event['list-name']
        username = event['username']
        # limit = int(event['limit'])
        # sort_key = event['sort-key']

        search_results = searchGroceryListNames(listname, username)
        return {
            "statusCode": 200,
            "body": search_results
        }
    except:
        return {
            "statusCode": 300,
            "message": "Serverside error"
        }

def searchGroceryListNames(listname, username, limit=10, sort_key='date-created'):
    """ Get names of grocery lists and locations based on listname,
        note listname may be incomplete, we use this to query table!

    Keyword Arguments
    listname -- The string the listname may begin with, ie
                for the lists ['thelist1', 'thelist2', 'avocadolist'],
                listname = 'the' selects 'thelist1', 'thelist2'.
    username -- The username of the account fetching the list
    """
    print("Location of lists that begin with:", listname, "sorted by", sort_key)
    ce = Key('username').eq(username)
    fe = Attr('list-name').begins_with(listname)
    response = table.query(
        KeyConditionExpression = ce,
        FilterExpression = fe
    )
    results = sorted(response["Items"], key=lambda x: x[sort_key])  # Sort items by specified attribute ie date-created
    results = results[:limit]                                       # Return only the amount of items specifed by limit
    return [json.dumps(res, cls=DecimalEncoder) for res in results]

def getGroceryListLocation(listname, username):
    """ Fetch list meta data from DynamoDB

    Keyword Arguments
    username -- The username of the account fetching the list
    listname -- the name of the grocery list in the DB
    """
    try:
        response = table.get_item(
            Key={
                'list-name': listname,
                #'username': username
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('response:', response)
        item = response['Item']
        return json.dumps(item, indent=4, cls=DecimalEncoder)

def convertTextFiletoGroceryListJson(location):
    """Get txt file from S3

    Keyword Arguments
    location -- the location of the file
    """
    pass # Implement


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

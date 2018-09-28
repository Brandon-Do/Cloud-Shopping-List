import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        phone_number = event['phone-number']
        list_name = event['list-name']
        list_items = event['items']

        if not is_valid_phone_number(phone_number):
            return {
                "statusCode": 400,
                "message":"Error, please format phone number: 0001112222"
            }
        phone_number = '+1' + phone_number # add country code
        text = format_json_for_text_message(list_name, list_items)
        send_str_to_phone(phone_number, text)
        return {
            "statusCode": 200,
            "message": "Success, sent {} to {}".format(list_name, phone_number)
        }
    except:
        return {
            "statusCode": 418,
            "message": "Serverside error"
        }


def send_str_to_phone(phone_number, text):
    """ send formatted text to phone via SNS

    Key Arguments
    text -- output of format_json_for_text_message(json)
    phone_number -- target phone, format: +1#########
    """
    sns.publish(
        PhoneNumber = phone_number,
        Message = text
    )

def format_json_for_text_message(list_name, list_items):
    """ formats list name and list items into string

    Key Arguments
    list_name -- The name of the list from input field frontend
    list_items -- Each row item on front end
    """
    text = ''
    input_fields = ['item-name', 'item-quantity', 'item-notes']
    if list_name:
        text += list_name + '\n'

    for item in list_items:
        text += get_key_values_from_item(input_fields, item)

    return text

def get_key_values_from_item(keys, item):
    """ To simplify above for loop. A helper function.
    """
    text = ''
    for key in keys:
        text += item[key] + ' '
    text += '\n'
    return text

def is_valid_phone_number(phone_number):
    """ Checks the validity of phone_number format

    Key Arguments
    phone_number -- from phone number input field on frontend
    """
    return phone_number.isdigit() and len(phone_number) == 10

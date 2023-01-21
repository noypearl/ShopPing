import json
import os
import helpers
import boto3


BUCKET_NAME = os.environ['BUCKET_NAME']
JSON_FILENAME = os.environ['JSON_FILENAME']

def get_boto_client():
    return boto3.client('s3')

# get user message like "list" and do all the magic to return a list
def user_message_to_bot_response(message):
    if message.startswith("/list") :
        return helpers.list_sites()
    elif message.startswith("/add"):
        arguments = message.split("€")
        keyword = arguments[1]
        url = arguments[2]
        return helpers.add_site(keyword, url)
    elif message.startswith("/resume"):
        arguments = message.split("€")
        site_id = str(arguments[1])
        print(f"request to resume id {site_id}")
        return helpers.resume_site(site_id)
    elif message.startswith("/delete"):
        arguments = message.split("€")
        site_id = str(arguments[1])
        print(f"request to delete id {site_id}")
        return helpers.delete_site(site_id)
    elif message.startswith("/stop"):
        arguments = message.split("€")
        site_id = str(arguments[1])
        print(f"request to stop id {site_id}")
        return helpers.stop_site(site_id)
    elif message.startswith("/help") or message.startswith("help"):
        return helpers.get_helper_message()
    else:
        return f"Unsupported command {message}.\n{helpers.get_helper_message()}"

def lambda_handler(event, context):
    print(f"event! {json.dumps(event)}")
    data = json.loads(event["body"])
    message = data["message"]
    text = str(message["text"])
    print(f"command::: {text}")
    try:
        bot_response = user_message_to_bot_response(text)
    except IndexError:
        print("Got invalid command")
        bot_response = "Got invalid command. Use € as a separator "
    helpers.send_bot_message(bot_response, )
    return {
    'statusCode': 200,
    'body': bot_response
    }

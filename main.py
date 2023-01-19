import os
import requests
from bs4 import BeautifulSoup
import json
import boto3
import flask
from flask import Flask, request, Response
import telegram
from telegram.ext import Updater, CommandHandler

BUCKET_NAME = os.environ['BUCKET_NAME']
JSON_FILENAME = os.environ['JSON_FILENAME']
chat_id = os.environ['chat_id']
API_TOKEN = os.environ['API_TOKEN']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_ACCESS_SECRET = os.environ['AWS_ACCESS_SECRET']
BASE_URL = "https://api.telegram.org/bot{}".format(API_TOKEN)


def lambda_func():
    event_body = request.get_data()
    data = json.loads(event_body["body"])
    message = data["message"]
    text = str(message["text"])

    chat_id = str(message["chat"]["id"])
    response = f"Got command: {text}"
    data = {"text": response, "chat_id": chat_id}
    url = BASE_URL + "/sendMessage"
    requests.post(url, data)
    # return {
    #     'statusCode': 200,
    #     'body': text
    # Verify the signature and process the event
    return Response(status=200)

def respond_to_webhook(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])

        response = f"Got command: {message}"

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)
        return message
    except Exception as e:
            print(e)
    return {"statusCode": 200}
# TODO- remove

def get_boto_client():
    # return boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_ACCESS_SECRET, region_name="us-east-1")
    return boto3.client('s3')
    # TODO: make use ACL / AWS  policy and not public bucket
#    TODO - remove hardcoded credentials
#  TODO restrict access point of s3 bucket to only from lambda ond not PUBLIC

def get_sites_array_from_s3():
    s3 = boto3.client('s3')
    s3_resource = s3.get_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME)
    json_data = json.loads(s3_resource.get('Body').read())
    print(json_data)
    return json_data

def list_sites():
    json_data = get_sites_from_s3()
    urls = []
    for index, site in enumerate(json_data):
        if site['enabled']:
            urls.append({index, site['url']})
    print(json)
    # bot.send_message(chat_id=update.message.chat_id, text='\n'.join(json.dumps(urls)))

def stop_site(bot, update, args):
    json_data = get_sites_from_s3()
    for site in json_data:
        if site['keyword'] == args[0]:
            site['enabled'] = False
            s3 = get_boto_client()
            s3.put_object(Bucket=BUCKET_NAME, Key='sites.json', Body=json.dumps(json_data))
            bot.send_message(chat_id=update.message.chat_id, text='Site {} stopped.'.format(site['url']))
            break

def resume_site(site_keyword):
    json_data = get_sites_from_s3()
    for site in json_data:
        if site['keyword'] == site_keyword:
            site['enabled'] = True
            s3 = get_boto_client()
            s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
            break

def sendBotMessage(text):
    chat_id = "856026537"
    data = {"text": text, "chat_id": chat_id}
    url = BASE_URL + "/sendMessage"
    requests.post(url, data=data)

def main():
    list_sites()

    # Telegram Bot Authorization Token
    # lambda_func()
    # updater = Updater(API_TOKEN)
    #
    # # Get the dispatcher to register handlers
    # dp = updater.dispatcher
    #
    # # Add command handler to list sites
    # dp.add_handler(CommandHandler("list", list_sites))
    #
    # # Add command handler to stop site
    # dp.add_handler(CommandHandler("stop", stop_site, pass_args=True))
    #
    # # Add command handler to stop site
    # dp.add_handler(CommandHandler("resume", resume_site, pass_args=True))
    #
    # # Start the Bot
    # updater.start_polling()
    #
    # # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # # SIGTERM or SIGABRT. This should be used most of the time, since
    # # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()

if __name__ == '__main__':
    main()

def is_in_stock(url, keyword):
    return 0
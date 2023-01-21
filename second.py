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
    print('connecting to s3')
    # return boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_ACCESS_SECRET, region_name="us-east-1")
    return boto3.client('s3')
    # TODO: make use ACL / AWS  policy and not public bucket
#    TODO - remove hardcoded credentials
#  TODO restrict access point of s3 bucket to only from lambda ond not PUBLIC

def get_sites_array_from_s3():
    s3 = boto3.client('s3')
    s3_resource = s3.get_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME)
    sites_array = json.loads(s3_resource.get('Body').read())
    return sites_array

def list_sites():
    sites_array = get_sites_array_from_s3()
    output = ""
    for index, site in enumerate(sites_array):
        # TODO find smarter way to do inline if althogh it's python
        status = "disabled"
        if site["enabled"] == "true":
            status = "enabled"
        output += f"{index} : \"{site['keyword']}\" keyword, {status} {site['url']}\n"
    # print(f"got sites list: {sites_array}")
    # print to user:
    print(output)
    # bot.send_message(chat_id=update.message.chat_id, text='\n'.join(json.dumps(urls)))

def stop_site(site_id):
    json_data = get_sites_array_from_s3()
    for i, site in enumerate(json_data):
        if str(i) == site_id:
            print(f"found site to stop: {site}")
            json_data[i]['enabled'] = "false"
            s3 = get_boto_client()
            s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
            # bot.send_message(chat_id=update.message.chat_id, text='Site {} stopped.'.format(site['url']))
            break


def resume_site(site_id):
    json_data = get_sites_array_from_s3()
    for i, site in enumerate(json_data):
        if str(i) == site_id:
            if site['enabled'] == "false":
                print(f"resuming site {site_id}")
                site['enabled'] = "true"
                s3 = get_boto_client()
                s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
                # TODO : print message to telegram chat
                break


def add_site(keyword, url):
    json_data = get_sites_array_from_s3()
    json_data.append({"url": url, "keyword": keyword, "enabled": "true"})
    print(f"adding new site : {keyword} {url}")
    s3 = get_boto_client()
    print(f"writing new json with added site to s3 bucket")
    s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
    print(f"Site was added successfully! it's enabled automatically, \nRun /list to see all sites")


def sendBotMessage(text):
    chat_id = "856026537"
    data = {"text": text, "chat_id": chat_id}
    url = BASE_URL + "/sendMessage"
    requests.post(url, data=data)


def print_helper():
    messsage = """Shopper - Telegram shopping bot! \n " 
    "supported commands: /list - see a list of all the sites\n" 
    /add [keyword] [url] - add new site with keyword to search and url of website"\n 
    "/resume [index] - resume the bot of a specific site by index from list"\n
    "/stop  - stop the bot of a specific site by index from list" """
    print(f"")

def main():
    message = os.environ['MESSAGE']
    #  TODO - use legit parser here to parse like a normal humanbeing and not like a peasant
    if message == "/list" :
        list_sites()
    elif message.startswith("/add"):
        arguments = message.split(" ")
        keyword = arguments[1]
        url = arguments[2]
        add_site(keyword, url)
    elif message.startswith("/resume"):
        arguments = message.split(" ")
        site_id = str(arguments[1])
        resume_site(site_id)
    elif message.startswith("/stop"):
        arguments = message.split(" ")
        site_id = str(arguments[1])
        stop_site(site_id)
    elif message == "/help":
        print_helper()
    else:
        print(f"Unsupported command.\n {message}")
        print_helper()
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

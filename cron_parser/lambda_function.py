import os
import requests
import boto3
import json

API_TOKEN = os.environ['API_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
BUCKET_NAME = os.environ['BUCKET_NAME']
JSON_FILENAME = os.environ['JSON_FILENAME']
BASE_URL = "https://api.telegram.org/bot{}".format(API_TOKEN)


def get_boto_client():
    print('connecting to s3')
    return boto3.client('s3')


def send_bot_message(text):
    data = {"text": text, "chat_id": CHAT_ID}
    url = BASE_URL + "/sendMessage"
    requests.post(url, data=data)


def get_sites_array_from_s3():
    s3 = boto3.client('s3')
    s3_resource = s3.get_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME)
    sites_array = json.loads(s3_resource.get('Body').read())
    return sites_array

def notify_if_hit(site_obj):
    if not site_obj['url'].startswith('http'):
        print(f"Site didn't start with URL - {site_obj['url']}.Skipping...")
        return
    if site_obj['enabled'] == "false":
        print(f"Site is disabled - {site_obj['url']}.Skipping..")
        return
    response = requests.get(site_obj['url'])
    if response.status_code == 200:
        html = response.text
        if site_obj['keyword'] in html:
            print(f"HIT! found in stock {site_obj['url']} with keyword {site_obj['keyword']}")
            send_bot_message(f"FOUND! {site_obj['url']}")

def lambda_handler(event, context):
    sites_json = get_sites_array_from_s3()
    for site in sites_json:
        notify_if_hit(site)
    return {
        'statusCode': 200,
        'body': 'ok'
    }

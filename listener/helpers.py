import json
import os
import requests
import boto3
from urllib.parse import urlparse

BUCKET_NAME = os.environ['BUCKET_NAME']
JSON_FILENAME = os.environ['JSON_FILENAME']
API_TOKEN = os.environ['API_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(API_TOKEN)
CHAT_ID = os.environ['CHAT_ID']


def get_boto_client():
    print('connecting to s3')
    return boto3.client('s3')


def get_sites_array_from_s3():
    s3 = boto3.client('s3')
    s3_resource = s3.get_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME)
    sites_array = json.loads(s3_resource.get('Body').read())
    return sites_array


def list_sites():
    sites_array = get_sites_array_from_s3()
    print(f"sites array: {sites_array}")
    output = ""
    for index, site in enumerate(sites_array):
        # TODO find smarter way to do inline if althogh it's python
        domain = urlparse(site['url']).netloc
        status = "disabled"
        if site["enabled"] == "true":
            status = "enabled"
        output += f"{index} : \"{site['keyword']}\" keyword, {status} {domain}\n"
    return output


def stop_site(site_id):
    json_data = get_sites_array_from_s3()
    for i, site in enumerate(json_data):
        if str(i) == site_id:
            print(f"found site to stop: {site}")
            if site["enabled"] == "true":
                json_data[i]['enabled'] = "false"
                print(f"json site in stop: {json_data}")
                s3 = get_boto_client()
                s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
                return f"Site with id {site_id} was stopped.\nRun /list to see all sites"
            else:
                return f"Site id {site_id} is already stopped"


def resume_site(site_id):
    json_data = get_sites_array_from_s3()
    for i, site in enumerate(json_data):
        if str(i) == site_id:
            if site['enabled'] == "false":
                print(f"resuming site {site_id}")
                json_data[i]['enabled'] = "true"
                print(f"json site in resume: {json_data}")
                s3 = get_boto_client()
                s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
                return f"Resumed site with id {site_id}\nRun /list to see all sites"
            else:
                return f"Site id {site_id} is already running.\nRun /list to see all sites"


def add_site(keyword, url):
    json_data = get_sites_array_from_s3()
    json_data.append({"url": url, "keyword": keyword, "enabled": "true"})
    print(f"adding new site : {keyword} {url}")
    s3 = get_boto_client()
    print("writing new json with added site to s3 bucket")
    s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
    return f"Site {url} was added successfully! it's enabled automatically, \nRun /list to see all sites"


def delete_site(site_id):
    json_data = get_sites_array_from_s3()
    for i, site in enumerate(json_data):
        if str(i) == site_id:
            print(f"found site to delete: {site}")
            del json_data[i]
            s3 = get_boto_client()
            print("Updating bucket after deleted site id {site_id}")
            s3.put_object(Bucket=BUCKET_NAME, Key=JSON_FILENAME, Body=json.dumps(json_data))
            return f"Site with id {site_id} was deleted.\nRun /list to see all sites"
    return f"Site id {site_id} isn't found. Are you trolling me?"


def send_bot_message(text):
    data = {"text": text, "chat_id": CHAT_ID}
    url = BASE_URL + "/sendMessage"
    requests.post(url, data=data)


def get_helper_message():
    message = "Shopper - Telegram shopping bot! \n\nThis bot takes url of website to check and keyword of out-of-stock meaning so that when this keyword won't exist in the website anymore - you'll get a notification and know that the item is in stock!!\nSupported commands:\n/list - see a list of all the sites\n/add [keyword] [url] - add new site with keyword of 'missing item' to search and url of website.\n/resume [index] - resume the bot of a specific site by index from list\n/stop [index]  - stop the bot of a specific site by index from list\n/delete [index]  - delete the bot of a specific site by index from list"
    return message

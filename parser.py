import os
import requests
from bs4 import BeautifulSoup

API_TOKEN = os.environ['API_TOKEN']
chat_id = os.environ['chat_id']

URL = "https://shop.waxman.co.il/product/%d7%9b%d7%a1%d7%90-%d7%90%d7%a8%d7%92%d7%95%d7%a0%d7%95%d7%9e%d7%99-%d7%9e%d7%a2%d7%95%d7%a6%d7%91-chic-%d7%91%d7%94%d7%99%d7%a8/"
#  special price URL to test : https://il.iherb.com/pr/nature-s-gate-biotin-bamboo-conditioner-for-thin-hair-16-fl-oz-473-ml/18757
# .find(id=super-special-price) . > b tag >  contains (sale price)

def send_telegram_message(message):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    return requests.post(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={message}", headers=headers)stop

# send URL of product and get the message to send - whether

def is_in_stock(url, keyword):


def lambda_handler(event, context):
    # load shoes page
    page = requests.get(URL).text
    soup = BeautifulSoup(page, "html.parser")
    # get current price
    # search for special section that only occurs when out of stock
    is_in_stock = soup.find_all("div", class_="in-stock")

    if is_in_stock:
        print(f"IN STOCK!  \n{URL} \n")
        message = f"IN STOCK!  \n{URL} \n"

        message_response = send_telegram_message(message)
        return {
            'statusCode': message_response.status_code,
            'body': message_response.text
        }
    else:
        return {
            'statusCode': 200,
            'body': 'Out of stock for my sizes'
        }

lambda_handler(1,1)
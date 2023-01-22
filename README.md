
# ShopPing
<img src="https://i.ibb.co/HNZDD1Y/Shop-Ping-logo.png" alt="drawing" width="200"/>

### In-Stock Pinging Telegram Bot Infrastructure In AWS

## Why
Because I'm lazy to check a website again and again and wait for an item to return back to stock <br>
**Read the full article about it [here](https://medium.com/@60noypearl/shopping-in-stock-pinging-telegram-bot-infrastructure-in-aws-13f545dc5f5)**


## TL;DR
This bot takes the url of an online item to monitor, and an out-of-stock word(s) keyword to search in the page, 
so that when this keyword won't exist in the page anymore - you'll get a notification 
from this bot and know that the item is back in stock!!

## Screenshots &  Video
!<img src="https://user-images.githubusercontent.com/11259340/213934806-2534dff9-5880-4a4f-a06f-029c5be04b17.jpeg" height="400" alt="bot screenshot"> !<img src="https://user-images.githubusercontent.com/11259340/213934912-7c5e0272-ba77-4196-8a5a-4acb03933a91.jpeg" height="400" alt="bot-screenshot">

### Full video [here](https://youtube.com/shorts/GZXChyn63ws)

## Components
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/2048px-Telegram_logo.svg.png" width="100"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Amazon_Lambda_architecture_logo.svg/1200px-Amazon_Lambda_architecture_logo.svg.png" width="100"> <img src="https://res.cloudinary.com/hy4kyit2a/f_auto,fl_lossy,q_70/learn/modules/monitoring-on-aws/monitor-your-architecture-with-amazon-cloudwatch/images/522c742e37be736db2af0f8a720b1c02_f-05-f-9-a-02-2-a-81-4-fa-3-b-651-412-e-2222-bd-08.png" width="100"><img src="https://cdn.iconscout.com/icon/free/png-256/amazon-s3-2968702-2464706.png" width="100"> <img src="https://awsvideocatalog.com/images/aws/png/PNG%20Light/Networking%20&%20Content%20Delivery/Amazon-API-Gateway.png" width="100"> <img src="https://avatars.githubusercontent.com/u/44036562?s=280&v=4" width="100">

- Telegram Bot - for managing the bots & getting notified when in-stock
- [AWS] Lambda x2 - one to listen to telegram messages and one to run periodically, parse websites
- [AWS] API Gateway - to allow external access from telegram to a lambda
- [AWS] CloudWatch - for logs & debugs
- [AWS] S3 Bucket x2 - one as a low-cost database & one for lambdas deployment
- GitHub repository with GitHub Actions - for automatic deployment of lambdas and not hating myself every time I need to deploy new code

## Environment
![environment](https://i.ibb.co/RQ0NPLF/undefined-2.png)


## Supported Commands
|Command|Description|
|-------------------------------|-----------------------------|
  |`/help`| Show help menu
  |`/list`|  Show monitored websites
  |`/add [keyword] [url] `| Add a website to monitor
  |`/stop [website_id]`| Stop monitoring a specific website
  |`/resume [website_id]`| Resume monitoring a specific website
  |`/delete [website_id]`| Add a website to monitor
  

## Files & directories
/listener - Lambda function code that's triggerred by the Telegram Webhook. 
<br>
/cron_parser - Lambda function code that parses each one of the monitored websites. Sends a message in Telegram when an item is back in stock.  
<br>
/.git/workflows/ - Two workflows for each one of the directories that run by path - for simlifying the deployment process.

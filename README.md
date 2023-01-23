
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

- Telegram [Bot](https://core.telegram.org/bots/tutorial) - for managing the bots & getting notified when in-stock
- [AWS] [Lambda](https://aws.amazon.com/lambda/) x2 - one to listen to telegram messages and one to run periodically, parse websites
- [AWS] [API Gateway](https://aws.amazon.com/api-gateway/) - to allow external access from telegram to a lambda
- [AWS] [CloudWatch](https://aws.amazon.com/cloudwatch/) - to see logs 
- [AWS] [S3 Bucket](https://aws.amazon.com/s3/) x2 - one as a low-cost database & one for lambdas deployment
- GitHub repository with [GitHub Actions](https://github.com/noypearl/Shopper/actions) - for automatic deployment of lambdas and not hating myself every time I need to deploy new code

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
  |`/delete [website_id]`| Delete a specific website from list
  

## Files & directories
/listener - Lambda function code that's triggerred by the Telegram Webhook. 
<br>
/cron_parser - Lambda function code that parses each one of the monitored websites. Sends a message in Telegram when an item is back in stock.  
/.git/workflows/ - Two workflows for each one of the directories that run by path - for simlifying the deployment process.

## Howto
In order to use the same AWS environment that I had, you need to setup a few things.
### Environment Variables / Secrets

|Component|Description|File
|-------------------------------|-----------------------------|-----------------------------|
  |Lambda|API_TOKEN|API Token from the Telegram bot - after you create a bot with [BotFather](https://core.telegram.org/bots/tutorial)|
  |Lambda|CHAT_ID| Telegram Bot [ChatID](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)|
  |Lambda|BUCKET_NAME|Name of S3 bucket that stores the sites JSON file
  |Lambda|JSON_FILENAME|Name of the JSON file in the S3 bucket (of BUCKET_NAME)
  |GitHub|AWS_ACCESS_KEY|Secret key stored in Github Actions Secrets Manager of the AWS user for deployment to AWS|
  |GitHub|AWS_SECRET_ACCESS_KEY|Secret stored in Github Actions Secrets Manager of the AWS user for deployment to AWS|
  |GitHub|AWS_REGION|Region in AWS to use for environment deployment|
  |GitHub|MENU_LAMBDA_FUNCTION_NAME|Name of 1st Lambda function that listens to Telegram messages (/listener directory code)|
  |GitHub|PARSER_LAMBDA_FUNCTION_NAME|Name of 2st Lambda function that runs every 1 hour to parse websitse and alert when new item in stock(/cron_parser directory code)|
  |GitHub|S3_DEPLOYMENT_BUCKET_NAME |The name of the S3 Bucket that will be used to upload zipped code for deployment|
  |GitHub|ZIP_LISTENER_FILENAME  |Name of the zip code that'll be genarated from /listener directory and deployed to Lambda|
  
  #### Files
  The JSON file that contains websites to parse looks like this:
  ```json
  [{
  "url": "https://we-are-cool-gamerz-with-swag.com/headphones?color=blue", 
  "keyword": "out-of-stock", 
  "enabled": "true"
  },
  {
  "url": "https://dog-hackers-stuff.com/paws_hoodie?color=black", 
  "keyword": "Unavailable", 
  "enabled": "false"
  }]
  ```
  You can create an empty one in your new S3 bucket / copy the one above for debugging.
  
  #### Roles & Permissions 
  Instead of listing the roles, permissions & policies - you should read the AWS docs about those to configure yourself because there are a lot and the best way to learn about those is by trial & error.
  
  #### Other configurations
  - API Gateway - configure that external call to its API will trigger the **menu** Lambda
  - Lambdas - 2 python-based lambdas with 2 layers: `requests` and `boto3`
  - EventBridge - configure that a scheduled event (e.g 1 hour) will trigger the **parser** Lambda
  - CloudWatch - I configured it to show extended logs from both API Gateway and the Lambdas. It saved me a ton of time during debugging of those components in the flow
  - S3 Bucket - configure 2 buckets - 1st for your sites.json file and 2nd for your deployment zipped code
  - S3 <-> Lambdas - you need to enable communication between your S3 sites.json bucket and your lambdas. Read about AWS policies to understand how
  
  #### screenshots of configurations
  <img src="https://user-images.githubusercontent.com/11259340/213937369-223c5b8f-6ce6-471b-81a7-bc45800fa01c.png" width="350" alt="cronjob lambda in aws"> <img src="https://user-images.githubusercontent.com/11259340/213937144-ea2c4461-3aa9-4eb4-a474-69087c60d5f9.png" width="350" alt="parser lambda in aws">

  <img src="https://user-images.githubusercontent.com/11259340/213937529-f18dbf4a-0e46-4496-8fc0-96be3dab2a64.png" width="350" alt="calling lambda from API Gateway"><img src="https://user-images.githubusercontent.com/11259340/213937627-6e8e64e9-a54f-4215-888f-2d85fdb2a447.png" width="350" alt="S3 deployment bucket">


  

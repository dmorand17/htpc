import requests
import os
import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Enable this for debugging requests
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1


def notify_slack(event):
    slackhook_url = os.getenv("SLACK_HOOK_URL")
    if slackhook_url is None:
        return {"status": "FAILED", "message": "Failed to invoke slack hook"}

    try:
        sns = event["Records"][0]["Sns"]
        message = json.loads(sns["Message"])
        message_detail = message.get("detail")
        notification_type = sns.get("Type")
        notification_title = message_detail.get("alarmName")
        notification_text = message_detail.get("state")["reason"]
        msg = f"*{notification_title}*\n\n`{notification_text}`"

    except KeyError as e:
        logger.error("Error handling event")
        return {"status": "failed"}
    data = {"text": msg}

    headers = {"content-type": "application/json"}
    r = requests.post(slackhook_url, headers=headers, data=json.dumps(data))
    if r.status_code == 200:
        logger.debug(f"response [SLACK] -> {r}, {r.text}")
        return {"status": "ok"}
    else:
        return {"status": "failed"}

def publish_sns(event):
    SNS_ARN = os.getenv("SNS_ARN")
    client = boto3.client("sns")
    resp = client.publish(TargetArn=SNS_ARN, Message=json.dumps(event,indent=2), Subject="HTPC Status Update")

    if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {"status": "ok"}
    else:
        return {"status": "failed"}

def lambda_handler(event, context):
    logger.debug("## ENVIRONMENT VARIABLES")
    logger.debug(os.environ)

    logger.debug("## EVENT")
    logger.debug(f"event-> {json.dumps(event)}")

    # Send event to slack channel
    response = notify_slack(event)

    # publish event to SNS queue to send email
    response = publish_sns(event)

    logger.debug("## RESPONSE")
    logger.debug(f"response [Lambda] -> {response}")

    return response

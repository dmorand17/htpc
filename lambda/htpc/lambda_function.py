import requests
import os
import logging
import json
import boto3
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Enable this for debugging requests
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1


def get_cloudwatch_alarm(event):
    sns_record = event["Records"][0]["Sns"]
    message = json.loads(sns_record["Message"])
    logger.info(f"message -> {json.dumps(message,indent=2)}")
    message_detail = message.get("detail")
    return {
        "title": message.get("detail-type"),
        "timestamp": message.get("Timestamp"),
        "state_value": message_detail.get("state")["value"],
        "state_reason": message_detail.get("state")["reason"],
    }


def notify_slack(event):
    slackhook_url = os.getenv("SLACK_HOOK_URL")
    if slackhook_url is None:
        return {"status": "FAILED", "message": "Failed to invoke slack hook"}

    try:
        cloudwatch_alarm = get_cloudwatch_alarm(event)
        msg = f"*[{cloudwatch_alarm['state_value']}]* {cloudwatch_alarm['title']}\n\n`{cloudwatch_alarm['state_reason']}`"

    except KeyError as e:
        logger.error("Error handling event")
        return {"status": "failed"}
    data = {"text": msg}

    headers = {"content-type": "application/json"}
    r = requests.post(slackhook_url, headers=headers, data=json.dumps(data))
    if r.status_code == 200:
        return {"status": "ok"}
    else:
        return {"status": "failed"}


def publish_sns(event):
    SNS_ARN = os.getenv("SNS_ARN")
    client = boto3.client("sns")
    cloudwatch_alarm = get_cloudwatch_alarm(event)
    timestamp = cloudwatch_alarm["timestamp"]
    msg = f"[{cloudwatch_alarm['state_value']}] {cloudwatch_alarm['title']}\n{cloudwatch_alarm['state_reason']}\n\n{json.dumps(event,indent=2)}"
    resp = client.publish(TargetArn=SNS_ARN, Message=msg, Subject=f"HTPC Update - {timestamp}")
    # client.close()

    if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {"status": "ok"}
    else:
        return {"status": "failed"}


def lambda_handler(event, context):
    logger.debug("## ENVIRONMENT VARIABLES")
    logger.debug(os.environ)

    logger.debug("## EVENT")
    logger.debug(f"event-> {json.dumps(event, indent=2)}")

    # Send event to slack channel
    response = notify_slack(event)

    # publish event to SNS queue to send email
    response = publish_sns(event)

    logger.debug("## RESPONSE")
    logger.debug(f"response [Lambda] -> {response}")

    return response

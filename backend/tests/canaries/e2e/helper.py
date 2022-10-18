import boto3
import os

# Useful for mocking lambda context object
class LambdaContext:
    aws_request_id = 'testing'


def upload_screenshot(request_id, driver, name):
    """Upload a screenshot to S3."""

    s3 = boto3.client('s3')
    driver.save_screenshot(f"/tmp/{name}.png")

    with open(f'/tmp/{name}.png', 'rb') as data:
        print(f"Uploading {name}.png to S3")
        s3.upload_fileobj(data, os.environ['S3_BUCKET'], f'{request_id}/{name}.png')
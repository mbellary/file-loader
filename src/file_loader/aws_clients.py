import aioboto3
import boto3
from file_loader.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_ID, S3_ENDPOINT_URL, SQS_ENDPOINT_URL, DYNAMODB_ENDPOINT_URL

# aioboto3 session
_session = aioboto3.Session(region_name=AWS_REGION)

# async clients factories
async def s3_client():
    return _session.client('s3',
                           region_name=AWS_REGION,
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
                           endpoint_url=S3_ENDPOINT_URL
                           )

async def sqs_client():
    return _session.client('sqs',
                           region_name=AWS_REGION,
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
                           endpoint_url=SQS_ENDPOINT_URL
                           )

async def dynamodb_client():
    return _session.client('dynamodb',
                           region_name=AWS_REGION,
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
                           endpoint_url=DYNAMODB_ENDPOINT_URL
                           )

def s3_boto_client():
    return boto3.client("s3",
                        region_name = AWS_REGION,
                        aws_access_key_id= AWS_ACCESS_KEY_ID,
                        aws_secret_access_key= AWS_SECRET_ACCESS_KEY_ID,
                        endpoint_url=S3_ENDPOINT_URL)

def sqs_boto_client():
    return boto3.client("sqs",
                        region_name = AWS_REGION,
                        aws_access_key_id= AWS_ACCESS_KEY_ID,
                        aws_secret_access_key= AWS_SECRET_ACCESS_KEY_ID,
                        endpoint_url=SQS_ENDPOINT_URL)

def dynamodb_boto_client():
    return boto3.client("dynamodb",
                        region_name = AWS_REGION,
                        aws_access_key_id= AWS_ACCESS_KEY_ID,
                        aws_secret_access_key= AWS_SECRET_ACCESS_KEY_ID,
                        endpoint_url=DYNAMODB_ENDPOINT_URL)

# For secrets we will use boto3 (sync)
# def get_secret_sync(secret_name):
#     client = boto3.client('secretsmanager', region_name=AWS_REGION)
#     resp = client.get_secret_value(SecretId=secret_name)
#     return resp.get('SecretString')



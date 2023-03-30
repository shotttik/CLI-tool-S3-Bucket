import boto3
from os import getenv
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import sys
from urllib.request import urlopen
from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)
load_dotenv()


class Client:

    def __init__(self, bucket_name=""):
        LOGGER.info('Creating the object')
        try:
            self.client = boto3.client(
                "s3",
                aws_access_key_id=getenv("aws_access_key_id"),
                aws_secret_access_key=getenv("aws_secret_access_key"),
                aws_session_token=getenv("aws_session_token"),
                region_name=getenv("aws_region_name")
            )
            self.bucket_name: str = bucket_name
            self.client.list_buckets()["Buckets"]
            LOGGER.info('object Created Successfully')

        except ClientError as e:
            LOGGER.error(e)
            sys.exit()
        except Exception:
            LOGGER.error("Unexpected error")
            sys.exit()

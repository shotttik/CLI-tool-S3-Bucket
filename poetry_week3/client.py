from hashlib import md5
from time import localtime
import boto3
from os import getenv
from dotenv import load_dotenv
import logging
from botocore.exceptions import ClientError
import json
import sys
from urllib.request import urlopen
import io
import magic

load_dotenv()


class Client(object):
    _instance = None

    def __new__(cls, bucket_name=""):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Client, cls).__new__(cls)
            try:
                cls.client = boto3.client(
                    "s3",
                    aws_access_key_id=getenv("aws_access_key_id"),
                    aws_secret_access_key=getenv("aws_secret_access_key"),
                    aws_session_token=getenv("aws_session_token"),
                    region_name=getenv("aws_region_name")
                )
                cls.bucket_name: str = bucket_name
                cls.client.list_buckets()["Buckets"]
            except ClientError as e:
                logging.error(e)
                sys.exit()
            except Exception:
                logging.error("Unexpected error")
                sys.exit()
        return cls._instance

    @classmethod
    def getInstance(cls):
        return cls._instance.client

    @classmethod
    def get_bucket_name(cls):
        return cls._instance.bucket_name

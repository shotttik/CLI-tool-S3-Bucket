from botocore.exceptions import ClientError
from client import Client
from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class Bucket_Crud:
    @staticmethod
    def buckets(s3_client) -> list | bool:
        try:
            return s3_client.client.list_buckets()["Buckets"]
        except ClientError as e:
            LOGGER.error(e)
            return False

    @classmethod
    def create_bucket(cls, s3_client, region="us-west-2") -> bool:
        if cls.__bucket_exists(s3_client):
            LOGGER.error("bucket already exists.")
            return False
        try:
            location = {"LocationConstraint": region}
            response = s3_client.client.create_bucket(
                Bucket=s3_client.bucket_name,
                CreateBucketConfiguration=location
            )
        except ClientError as e:
            LOGGER.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            print("bucket created successfully")
            return True
        return False

    @classmethod
    def delete_bucket(cls, s3_client) -> bool:
        if cls.__bucket_exists(s3_client.client) is False:
            LOGGER.error("bucket doesn't exists.")
            return False
        try:
            response = s3_client.client.delete_bucket(
                Bucket=s3_client.client)
        except ClientError as e:
            LOGGER.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            LOGGER.info("bucker deleted successfully")
            return True
        return False

    @staticmethod
    def __bucket_exists(s3_client) -> bool:
        try:
            response = s3_client.client.head_bucket(
                Bucket=s3_client.bucket_name)
        except ClientError as e:
            LOGGER.info(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

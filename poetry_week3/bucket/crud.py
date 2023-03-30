import logging
from botocore.exceptions import ClientError
from client import Client


class Bucket_Crud:
    @staticmethod
    def buckets() -> list | bool:
        try:
            return Client().getInstance().list_buckets()["Buckets"]
        except ClientError as e:
            logging.error(e)
            return False

    @classmethod
    def create_bucket(cls, region="us-west-2") -> bool:
        if cls.__bucket_exists:
            logging.error("bucket already exists.")
            return False
        try:
            location = {"LocationConstraint": region}
            response = Client().getInstance().create_bucket(
                Bucket=Client().get_bucket_name(),
                CreateBucketConfiguration=location
            )
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            print("bucket created successfully")
            return True
        return False

    @classmethod
    def delete_bucket(cls) -> bool:
        if cls.__bucket_exists() is False:
            logging.error("bucket doesn't exists.")
            return False
        try:
            response = Client().getInstance().delete_bucket(
                Bucket=Client().get_bucket_name())
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            logging.INFO("bucker deleted successfully")
            return True
        return False

    @staticmethod
    def __bucket_exists() -> bool:
        try:
            response = Client().getInstance().head_bucket(
                Bucket=Client().get_bucket_name())
        except ClientError as e:
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

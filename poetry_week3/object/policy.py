import logging
from botocore.exceptions import ClientError
from client import Client
from poetry_week3.bucket.crud import Bucket_Crud
from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class Object_Policy:
    @staticmethod
    def set_object_access_policy(s3_client, file_name):
        try:
            response = s3_client.client.put_object_acl(
                ACL="public-read",
                Bucket=s3_client.bucket_name,
                Key=file_name
            )
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

    @staticmethod
    def put_lifecycle_policy(s3_client):
        lfc = {
            "Rules": [
                {
                    "Expiration": {"Days": 120},
                    "ID": "devobjects",
                    "Filter": {"Prefix": "dev"},
                    "Status": "Enabled",
                }
            ]
        }
        s3_client.client.put_bucket_lifecycle_configuration(
            Bucket=s3_client.bucket_name, LifecycleConfiguration=lfc
        )
        LOGGER.info("life cycle policy added successfully")

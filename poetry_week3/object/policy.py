import logging
from botocore.exceptions import ClientError
from client import Client


class Object_Policy:
    @staticmethod
    def set_object_access_policy(file_name):
        try:
            response = Client().getInstance().put_object_acl(
                ACL="public-read",
                Bucket=Client().get_bucket_name().bucket_name,
                Key=file_name
            )
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

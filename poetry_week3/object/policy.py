import logging
from botocore.exceptions import ClientError
from client import Client


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

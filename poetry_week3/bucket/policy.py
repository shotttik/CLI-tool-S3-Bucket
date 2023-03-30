import json
import logging
from botocore.exceptions import ClientError

from poetry_week3.client import Client


class Bucket_Policy:

    @staticmethod
    def __generate_public_read_policy():
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{Client().get_bucket_name()}/*",
                }
            ],
        }

        return json.dumps(policy)

    @staticmethod
    def __generate_multiple_policy():
        policy = {
            "Version":
            "2012-10-17",
            "Statement": [{
                "Action": [
                    "s3:PutObject", "s3:PutObjectAcl", "s3:GetObject", "s3:GetObjectAcl",
                    "s3:DeleteObject"
                ],
                "Resource":
                [f"arn:aws:s3:::{Client().get_bucket_name()}",
                 f"arn:aws:s3:::{Client().get_bucket_name()}/*"],
                "Effect":
                "Allow",
                "Principal":
                "*"
            }]
        }

        return json.dumps(policy)

    @classmethod
    def assign_policy(cls, policy_function):
        policy = None
        if policy_function == "public_read_policy":
            policy = cls.__generate_public_read_policy()
        elif policy_function == "multiple_policy":
            policy = cls.__generate_multiple_policy()

        if (not policy):
            print('please provide policy')
            return

        Client().getInstance().put_bucket_policy(
            Bucket=Client().get_bucket_name(), Policy=policy)
        print("Bucket multiple policy assigned successfully")

    @staticmethod
    def read_bucket_policy():
        policy = Client().getInstance().get_bucket_policy(
            Bucket=Client().get_bucket_name())

        status_code = policy["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return policy["Policy"]
        return False

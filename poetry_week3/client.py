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


class S3_BUCKET():

    def __init__(self, bucket_name: str = "") -> None:
        try:
            self.client = boto3.client(
                "s3",
                aws_access_key_id=getenv("aws_access_key_id"),
                aws_secret_access_key=getenv("aws_secret_access_key"),
                aws_session_token=getenv("aws_session_token"),
                region_name=getenv("aws_region_name")
            )
            self.bucket_name: str = bucket_name
            self.buckets
        except ClientError as e:
            logging(e)
            sys.exit()
        except Exception:
            logging.error("Unexpected error")
            sys.exit()

    @property
    def buckets(self) -> list | bool:
        try:
            return self.client.list_buckets()["Buckets"]
        except ClientError as e:
            logging.error(e)
            return False

    def create_bucket(self, region="us-west-2") -> bool:
        if self.__bucket_exists:
            logging.error("bucket already exists.")
            return False
        try:
            location = {"LocationConstraint": region}
            response = self.client.create_bucket(
                Bucket=self.bucket_name,
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

    def delete_bucket(self) -> bool:
        if self.__bucket_exists() is False:
            logging.error("bucket doesn't exists.")
            return False
        try:
            response = self.client.delete_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            logging.INFO("bucker deleted successfully")
            return True
        return False

    def __generate_public_read_policy(self):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                }
            ],
        }

        return json.dumps(policy)

    def create_bucket_policy(self):
        self.aws_s3_client.put_bucket_policy(
            Bucket=self.bucket_name, Policy=self.__generate_public_read_policy(
                self.bucket_name)
        )
        print("Bucket policy created successfully")

    def read_bucket_policy(self):
        if self.__policy_exists() is False:
            return False
        try:
            policy = self.client.get_bucket_policy(Bucket=self.bucket_name)
            policy_str = policy["Policy"]
            print(policy_str)
        except ClientError as e:
            logging.error(e)
            return False

    def download_file_and_upload_to_s3(self, url, file_name="", keep_local=False):

        with urlopen(url) as response:
            content = response.read()
            allowed_files = [
                "image/jpeg",
                "image/bmp",
                "image/png",
                "image/webp",
                "video/mp4"
            ]
            try:
                mime_type = magic.from_buffer(content, mime=True)
                type_format = mime_type.split("/")[1]
                if mime_type not in allowed_files:
                    logging.error("Invalid file type.")
                    return False

                if file_name == "":
                    file_name = f'image_file_{md5(str(localtime()).encode("utf-8")).hexdigest()}.{type_format}'
                    # avoiding issue if user entered wrong file type format
                if '.' in file_name and not file_name.endswith(type_format):
                    wrong_type_format = file_name[file_name.find(".")+1:]
                    file_name = file_name.replace(
                        wrong_type_format, type_format)
                if '.' not in file_name:
                    file_name += "." + type_format

                self.client.upload_fileobj(
                    Fileobj=io.BytesIO(content),
                    Bucket=self.bucket_name,
                    ExtraArgs={'ContentType': mime_type},
                    Key=file_name
                )
            except Exception as e:
                logging.error(e)

        if keep_local:
            with open('resources/'+file_name, mode='wb') as jpg_file:
                jpg_file.write(content)

        # public URL
        return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            'us-west-2',
            self.bucket_name,
            file_name
        )

    def set_object_access_policy(self, file_name):
        try:
            response = self.client.put_object_acl(
                ACL="public-read",
                Bucket=self.bucket_name,
                Key=file_name
            )
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

    def __bucket_exists(self) -> bool:
        try:
            response = self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

    def __policy_exists(self) -> bool:
        try:
            response = self.client.get_bucket_policy(Bucket=self.bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
        return False

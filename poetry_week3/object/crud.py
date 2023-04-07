import datetime
from botocore.exceptions import ClientError
from client import Client
from hashlib import md5
from time import localtime
from os import getenv
from urllib.request import urlopen
import io
import magic
import os
import boto3
from botocore.config import Config

from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class Object_Crud:

    @staticmethod
    def get_objects(s3_client):
        for key in s3_client.client.list_objects(Bucket=s3_client.bucket_name)['Contents']:
            print(f" {key['Key']}, size: {key['Size']}")

    @staticmethod
    def delete_object(s3_client, filename: str):
        s3_client.client.delete_object(
            Bucket=s3_client.bucket_name, Key=filename)
        LOGGER.info("Deletet object " + filename + " Successfully")

    @staticmethod
    def download_file_and_upload_to_s3(s3_client, url, file_name="", keep_local=False):

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
                    LOGGER.error("Invalid file type.")
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

                s3_client.client.upload_fileobj(
                    Fileobj=io.BytesIO(content),
                    Bucket=s3_client.bucket_name,
                    ExtraArgs={'ContentType': mime_type},
                    Key=file_name
                )
            except Exception as e:
                LOGGER.error(e)

        if keep_local:
            with open('resources/'+file_name, mode='wb') as jpg_file:
                jpg_file.write(content)

        # public URL
        return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            'us-west-2',
            s3_client.bucket_name,
            file_name
        )

    # მცირე ზომის ფაილების ატვირთვა

    @staticmethod
    def upload_file(s3_client, file_name):
        response = s3_client.client.upload_file(
            file_name, s3_client.bucket_name, 'hello.txt')
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            LOGGER.info("uploaded successfully.")
            return True
        LOGGER.error("upload failed.")
        return False

    # დიდი ზომის ფაილების ატვირთვა
    @staticmethod
    def multipart_upload(s3_client, filename, key, PART_BYTES=1024 * 10):
        mpu = s3_client.client.create_multipart_upload(
            Bucket=s3_client.bucket_name, Key=key)
        mpu_id = mpu["UploadID"]

        parts = []
        uploaded_bytes = 0
        total_bytes = os.stat(filename).st_size

        with open(filename, "rb") as f:
            i = 1
            while uploaded_bytes != total_bytes:
                data = f.read(PART_BYTES)
                part = s3_client.client.upload_part(Body=data, Bucket=s3_client.bucket_name, Key=key, UploadId=mpu_id,
                                                    PartNumber=i)
                parts.append({"PartNumber": i, "ETag": part["ETag"]})
                uploaded_bytes += len(data)
                print("{0} of {1} uploaded".format(
                    uploaded_bytes, total_bytes))
                i += 1
        result = s3_client.complete_multipart_upload(
            Bucket=s3_client.bucket_name, Key=key, UploadId=mpu_id, MultipartUpload={
                "Parts": parts}
        )
        LOGGER.info(result)
        return result

    @staticmethod
    def delete_file_versions_older_6_month(s3_client, prefix):
        versions = s3_client.client.list_object_versions(
            Bucket=s3_client.bucket_name, Prefix=prefix)

        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=180)

        for version in versions['Versions']:
            last_modified = version['LastModified']

            if last_modified < cutoff_date:
                s3_client.client.delete_object(Bucket=s3_client.bucket_name,
                                               Key=version['Key'], VersionId=version['VersionId'])
                LOGGER.info(f"Deleted versions of {prefix} older than 6 month")


'''
    @staticmethod
    def upload_file_obj(s3_client, filename):
        with open(filename, "rb") as file:
            s3_client.client.upload_fileobj(file, "hello_obj.txt")

    @staticmethod
    def upload_file_put(s3_client, filename):
        with open(filename, "rb") as file:
            s3_client.client.put_object(Bucket=s3_client.bucket_name,
                                        Key="hello_put.txt",
                                        Body=file.read())
'''

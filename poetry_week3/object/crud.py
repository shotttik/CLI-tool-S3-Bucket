from botocore.exceptions import ClientError
from client import Client
from hashlib import md5
from time import localtime
from os import getenv
from urllib.request import urlopen
import io
import magic

from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class Object_Crud:
    @staticmethod
    def download_file_and_upload_to_s3(url, file_name="", keep_local=False):

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

                Client().getInstance().upload_fileobj(
                    Fileobj=io.BytesIO(content),
                    Bucket=Client().get_bucket_name(),
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
            Client().get_bucket_name(),
            file_name
        )

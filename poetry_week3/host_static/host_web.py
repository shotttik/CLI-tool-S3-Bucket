import os
from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class Host:
    @staticmethod
    def host_website(s3_client, source):
        LOGGER.info("hosting started...")
        index_file = 'index.html'
        error_file = 'error.html'

        # Upload the static files to the S3 bucket
        for root, dirs, files in os.walk(f'static-files/{source}'):
            for filename in files:
                filepath = os.path.join(root, filename)
                key = os.path.relpath(filepath, f'static-files/{source}')
                s3_client.client.upload_file(
                    filepath, s3_client.bucket_name, key)

        # Configure the bucket for static website hosting
        s3_client.client.put_bucket_website(Bucket=s3_client.bucket_name,
                                            WebsiteConfiguration={
                                                'IndexDocument': {'Suffix': index_file},
                                                # 'ErrorDocument': {'Key': error_file}
                                            })

        # Retrieve the website endpoint URL
        public_url = "http://{0}.s3-website-{1}.amazonaws.com".format(
            s3_client.bucket_name, os.getenv("aws_s3_region_name", "us-west-2"))

        LOGGER.info(f"hosting finished... {public_url}")

        print(f"The website is hosted at: {public_url}")

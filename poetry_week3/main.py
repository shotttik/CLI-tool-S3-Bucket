from dotenv import load_dotenv
import argparse
from poetry_week3.bucket.crud import Bucket_Crud
from poetry_week3.bucket.policy import Bucket_Policy
from poetry_week3.client import Client
from poetry_week3.object.crud import Object_Crud
from poetry_week3.object.policy import Object_Policy

from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)
load_dotenv()


def main(command_line=None):
    parser = argparse.ArgumentParser('AWS S3 Client BTU TASK')
    parser.add_argument(
        '--showBuckets',
        action='store_true',
        help='Print buckets'
    )
    subparsers = parser.add_subparsers(dest='command')
    bucket = subparsers.add_parser('bucket', help='work with bucket')
    bucket.add_argument(
        '--name',
        type=str, help="Enter Bucket Name", required=True
    )

    group = bucket.add_mutually_exclusive_group()
    group.add_argument('--createBucket', action='store_true')
    group.add_argument('--deleteBucket', action='store_true')
    group.add_argument('--showPolicy', action='store_true')
    group.add_argument("-arp",
                       "--assign_read_policy",
                       help="flag to assign read bucket policy.",
                       choices=[
                            "False", "True"],
                       type=str,
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument("-amp",
                       "--assign_missing_policy",
                       help="flag to assign read bucket policy.",
                       choices=["False", "True"],
                       type=str,
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument("-lo",
                       "--list_objects",
                       type=str,
                       help="list bucket object",
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument("-ufd",
                       "--upload_file_dir",
                       type=str,
                       help="Upload file from directory",
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument("-mu",
                       "--multipart_upload",
                       type=str,
                       help="Upload big file from directory, multipart upload.",
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument("-plp",
                       "--put_lifecycle_policy",
                       type=str,
                       help="configuration of lifecicly, delete after 120 days.",
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument('-makePublic', '-mp', '--makePublic',  action='store_true',
                       help="make Public(read) file", dest="makePublic")
    group.add_argument('--uploadFile', type=str,
                       help="Enter file url.",)
    bucket.add_argument('--key', type=str,
                        help="Enter key for uploading multipart. big files.!")
    bucket.add_argument('--filename', type=str,
                        help="Enter File name format for uploading.")
    bucket.add_argument('-save', '-s', '--save',  action='store_true',
                        help="Keep/Save local when uploading image", dest="save")

    args = parser.parse_args(command_line)

    if args.showBuckets:
        s3_client = Client()
        buckets = Bucket_Crud.buckets(s3_client)
        if buckets:
            for bucket in buckets:
                print(f' {bucket["Name"]}')

    if args.command == 'bucket':
        s3_client = Client(args.name)
        if args.createBucket:
            Bucket_Crud.create_bucket(s3_client)
        if args.showPolicy:
            Bucket_Policy.read_bucket_policy(s3_client)
        if args.deleteBucket:
            Bucket_Crud.delete_bucket(s3_client)
        if args.assign_read_policy == "True":
            Bucket_Policy.assign_policy(
                s3_client, "public_read_policy")
        if args.assign_missing_policy == "True":
            Bucket_Policy.assign_policy(
                s3_client, "multiple_policy")
        if args.list_objects == "True":
            Object_Crud.get_objects(s3_client)

        if args.upload_file_dir:
            if args.filename:
                Object_Crud.upload_file(s3_client, args.filename)

        if args.multipart_upload:
            if args.filename and args.key:
                Object_Crud.multipart_upload(
                    s3_client, args.filename, args.key)

        if args.put_lifecycle_policy:
            Object_Policy.put_lifecycle_policy(s3_client)

        if args.uploadFile:
            file_name = ""
            if args.filename:
                file_name = args.filename
            Object_Crud.download_file_and_upload_to_s3(
                s3_client, args.uploadFile, file_name, keep_local=args.save)
        if args.makePublic and args.filename:
            Object_Policy.set_object_access_policy(s3_client, args.filename)


if __name__ == "__main__":
    main()

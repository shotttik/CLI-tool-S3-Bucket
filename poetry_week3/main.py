from dotenv import load_dotenv
import argparse
from poetry_week3.client import S3_BUCKET


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
    group.add_argument('--createPolicy', action='store_true')
    group.add_argument('-makePublic', '-mp', '--makePublic',  action='store_true',
                       help="make Public(read) file", dest="makePublic")
    group.add_argument('--uploadFile', type=str,
                       help="Enter file url.",)
    bucket.add_argument('--filename', type=str,
                        help="Enter File name format for uploading.")
    bucket.add_argument('-save', '-s', '--save',  action='store_true',
                        help="Keep/Save local when uploading image", dest="save")

    args = parser.parse_args(command_line)

    if args.showBuckets:
        s3_client = S3_BUCKET()
        buckets = s3_client.buckets
        if buckets:
            for bucket in buckets:
                print(f' {bucket["Name"]}')

    if args.command == 'bucket':
        s3_client = S3_BUCKET(args.name)
        if args.createBucket:
            s3_client.create_bucket()
        if args.showPolicy:
            s3_client.read_bucket_policy()
        if args.deleteBucket:
            s3_client.delete_bucket()
        if args.createPolicy:
            s3_client.create_bucket_policy()
        if args.uploadFile:
            file_name = ""
            if args.filename:
                file_name = args.filename
            s3_client.download_file_and_upload_to_s3(
                args.uploadFile, file_name, keep_local=args.save)
        if args.makePublic and args.filename:
            print(args.filename)
            s3_client.set_object_access_policy(args.filename)


if __name__ == "__main__":
    main()

import time
from dotenv import load_dotenv
import argparse
from poetry_week3.bucket.crud import Bucket_Crud
from poetry_week3.bucket.policy import Bucket_Policy
from poetry_week3.client import Client
from poetry_week3.instance.crud import EC2_Crud
from poetry_week3.my_args import host_arguments, instance_arguments, vpc_arguments
from poetry_week3.object.crud import Object_Crud
from poetry_week3.object.policy import Object_Policy
from poetry_week3.host_static.host_web import Host
from poetry_week3.logger import CustomLogger
from poetry_week3.vpc.crud import Vpc_Crud

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
    host = host_arguments(subparsers.add_parser(
        "host", help="work with host/ing"))

    vpc = vpc_arguments(subparsers.add_parser(
        "vpc", help="work with vpc"))

    instance = instance_arguments(subparsers.add_parser(
        "instance", help="work with instance/vpc"))

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
                       action='store_true',
                       dest="assign_read_policy",
                       help="flag to assign read bucket policy.",
                       )

    group.add_argument("-amp",
                       "--assign_missing_policy",
                       action='store_true',
                       dest="assign_missing_policy",
                       help="flag to assign read bucket policy.",
                       )

    group.add_argument("-lo",
                       "--list_objects",
                       action='store_true',
                       dest="list_objects",
                       help="list bucket object",
                       )

    group.add_argument("-ufd",
                       "--upload_file_dir",
                       action='store_true',
                       dest="upload_file_dir",
                       help="Upload file from directory",
                       )

    group.add_argument("-mu",
                       "--multipart_upload",
                       action='store_true',
                       dest="multipart_upload",
                       help="Upload big file from directory, multipart upload.",

                       )

    group.add_argument("-plp",
                       "--put_lifecycle_policy",
                       action='store_true',
                       dest="put_lifecycle_policy",
                       help="configuration of lifecicly, delete after 120 days.",
                       )

    group.add_argument("-del",
                       "--delete_object",
                       action='store_true',
                       dest="delete_object",
                       help="delete object file")

    group.add_argument('-makePublic', '-mp', '--makePublic',  action='store_true',
                       help="make Public(read) file", dest="makePublic")
    group.add_argument('--uploadFile', type=str,
                       help="Enter file url.",)
    group.add_argument('--deleteVersions', '-dv', '-deleteVersions', action='store_true',
                       help='delete oject versions older than 6 motnh', dest='deleteVersions')
    group.add_argument('--uploadany', '-up', '-uploadany', action='store_true',
                       help='delete oject versions older than 6 motnh', dest='uploadany')
    bucket.add_argument('--key', type=str,
                        help="Enter key for uploading multipart. big files.!")
    bucket.add_argument('--filename', type=str,
                        help="Enter File name for uploading.")
    bucket.add_argument('--filepath', '-path', '-fp', dest='filepath', type=str,
                        help="Enter File path for uploading any format files.")
    bucket.add_argument('--prefix', '-prefix', '-pr', dest='prefix', type=str,
                        help="Enter prefix/filename/foldername for deleting versions.")

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
        if args.assign_read_policy:
            Bucket_Policy.assign_policy(
                s3_client, "public_read_policy")
        if args.assign_missing_policy:
            Bucket_Policy.assign_policy(
                s3_client, "multiple_policy")
        if args.list_objects:
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

        if args.delete_object and args.filename:
            Object_Crud.delete_object(s3_client, args.filename)

        if args.uploadFile:
            file_name = ""
            if args.filename:
                file_name = args.filename
            Object_Crud.download_file_and_upload_to_s3(
                s3_client, args.uploadFile, file_name, keep_local=args.save)

        if args.deleteVersions and args.prefix:
            Object_Crud.delete_file_versions_older_6_month(
                s3_client, args.prefix)
        if args.uploadany and args.filepath:
            Object_Crud.upload_any_format_object(s3_client, args.filepath)

        if args.makePublic and args.filename:
            Object_Policy.set_object_access_policy(s3_client, args.filename)
    if args.command == 'host':
        s3_client = Client(args.bucket_name)
        if args.source:
            Host.host_website(s3_client, args.source)
    if args.command == 'vpc':
        s3_client = Client(args.bucket_name)
        if args.tag and not args.quantity:
            Vpc_Crud.self_create(s3_client, args.tag)
        if args.tag and args.quantity:
            Vpc_Crud.full_self_create(s3_client, args.tag, int(args.quantity))
    if args.command == "instance":
        if args.vpcid and args.subnetid:
            s3_client = Client()
            security_group_id = Vpc_Crud.create_security_group(s3_client,
                                                               "ec2-sg", "Security group to enable access on ec2", args.vpcid)
            Vpc_Crud.open_http_traffic_from_all_ip(
                s3_client, security_group_id)
            local_ip = Vpc_Crud.get_my_public_ip()
            Vpc_Crud.authorize_inbound_shh_traffic(
                s3_client, security_group_id, local_ip)
            instance_id = EC2_Crud.run_ec2(security_group_id, args.subnetid,
                                           'btu-custom-instance')
            time.sleep(10)
            public_ip = EC2_Crud.assing_public_ip_to_instance(
                s3_client, instance_id)
            time.sleep(5)
            EC2_Crud.check_accessibility_of_the_instance(public_ip)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        LOGGER.error(e)

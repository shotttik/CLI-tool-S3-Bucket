
import paramiko
from poetry_week3.logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class EC2_Crud:

    @staticmethod
    def run_ec2(s3_client, sg_id, subnet_id, instance_name):
        response = s3_client.client.run_instances(
            BlockDeviceMappings=[
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeSize": 10,
                        "VolumeType": "gp2",
                        "Encrypted": False
                    },
                },
            ],
            ImageId="ami-053b0d53c279acc90",
            InstanceType="t2.micro",
            KeyName="MyKeyPair",
            MaxCount=1,
            MinCount=1,
            Monitoring={"Enabled": True},
            # SecurityGroupIds=[
            #     sg_id,
            # ],
            # SubnetId=subnet_id,
            UserData="""#!/bin/bash
        echo "Hello I am from user data" > info.txt
        """,
            InstanceInitiatedShutdownBehavior="stop",
            NetworkInterfaces=[
                {
                    "AssociatePublicIpAddress": True,
                    "DeleteOnTermination": True,
                    "Groups": [
                        sg_id,
                    ],
                    "DeviceIndex": 0,
                    "SubnetId": subnet_id,
                },
            ],
        )

        for instance in response.get("Instances"):
            instance_id = instance.get("InstanceId")
            print("InstanceId - ", instance_id)
        # pprint(response)

        # Create a name tag for the instance
        tag = {'Key': 'Name', 'Value': instance_name}

        # Assign the name tag to the instance
        s3_client.client.create_tags(Resources=[instance_id], Tags=[tag])

        return instance_id

    @staticmethod
    def stop_ec2(s3_client, instance_id):
        response = s3_client.client.stop_instances(InstanceIds=[
            instance_id,
        ], )
        for instance in response.get("StoppingInstances"):
            print("Stopping instance - ", instance.get("InstanceId"))

    @staticmethod
    def start_ec2(s3_client, instance_id):
        response = s3_client.client.start_instances(InstanceIds=[
            instance_id,
        ], )
        for instance in response.get("StartingInstances"):
            print("Starting instance - ", instance.get("InstanceId"))

    @staticmethod
    def terminate_ec2(s3_client, instance_id):
        response = s3_client.client.terminate_instances(InstanceIds=[
            instance_id,
        ], )
        for instance in response.get("TerminatingInstances"):
            print("Terminating instance - ", instance.get("InstanceId"))

    @staticmethod
    def assing_public_ip_to_instance(s3_client, instance_id):
        LOGGER.info("ssociate a public IP address with the instance")
        # Associate a public IP address with the instance
        s3_client.client.modify_instance_attribute(
            InstanceId=instance_id,
            SourceDestCheck={'Value': False}
        )

        # Allocate an Elastic IP address
        elastic_ip_response = s3_client.client.allocate_address(Domain='vpc')
        allocation_id = elastic_ip_response['AllocationId']

        # Associate the Elastic IP address with the instance
        s3_client.client.associate_address(
            InstanceId=instance_id,
            AllocationId=allocation_id
        )

        # Retrieve the public IP address of the instance
        response = s3_client.client.describe_instances(
            InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        return public_ip

    @staticmethod
    def check_accessibility_of_the_instance(public_ip, key_name="MyKeyPair"):
        LOGGER.info("# Check accessibility of the instance.")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=public_ip,
                username='ec2-user',
                key_filename=f'{key_name}.pem'
            )
            print('EC2 instance is accessible via SSH.')
        except Exception as e:
            print('Unable to connect to the EC2 instance via SSH:', str(e))
        finally:
            ssh_client.close()

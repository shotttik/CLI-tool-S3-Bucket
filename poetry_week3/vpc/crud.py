from poetry_week3.logger import CustomLogger


LOGGER = CustomLogger.get_logger(__name__)


class Vpc_Crud:
    @staticmethod
    def list_vpcs(ec2_client):
        result = ec2_client.client.describe_vpcs()
        vpcs = result.get("Vpcs")
        print(vpcs)

    @staticmethod
    def create_vpc(ec2_client):
        result = ec2_client.client.create_vpc(CidrBlock="10.0.0.0/16")
        vpc = result.get("Vpc")
        print(vpc)
        LOGGER.info(f"created vpc")

        return vpc.get("VpcId")

    @staticmethod
    def add_name_tag(ec2_client, vpc_id, tag):
        ec2_client.client.create_tags(Resources=[vpc_id],
                                      Tags=[{
                                          "Key": "Name",
                                          "Value": tag
                                      }])
        LOGGER.info(f"added name tage", tag)

    @staticmethod
    def create_igw(ec2_client):
        result = ec2_client.client.create_internet_gateway()
        LOGGER.info(f"created igw")
        return result.get("InternetGateway").get("InternetGatewayId")

    @staticmethod
    def attach_igw_to_vpc(ec2_client, vpc_id, igw_id):
        ec2_client.client.attach_internet_gateway(
            InternetGatewayId=igw_id, VpcId=vpc_id)
        LOGGER.info(f"atteached igw -{igw_id} to vpc-{vpc_id}")

    @classmethod
    def self_create(cls, tag: str):
        cls.list_vpcs()
        vpc_id = cls.create_vpc()
        print(cls.add_name_tag(vpc_id, tag))
        igw_id = cls.create_igw()
        cls.attach_igw_to_vpc(vpc_id, igw_id)
        LOGGER.info(f"self create finished")

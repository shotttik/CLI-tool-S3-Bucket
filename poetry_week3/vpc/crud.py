import pprint
import time
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
    def self_create(cls,  ec2_client, tag: str):
        cls.list_vpcs(ec2_client)
        vpc_id = cls.create_vpc(ec2_client)
        print(cls.add_name_tag(ec2_client, vpc_id, tag))
        igw_id = cls.create_igw()
        cls.attach_igw_to_vpc(ec2_client, vpc_id, igw_id)
        LOGGER.info(f"self create finished")

    @staticmethod
    def create_subnet(ec2_client, vpc_id, cidr_block, subnet_name):
        response = ec2_client.client.create_subnet(
            VpcId=vpc_id, CidrBlock=cidr_block)
        subnet = response.get("Subnet")
        pprint(subnet)
        subnet_id = subnet.get("SubnetId")
        time.sleep(2)
        ec2_client.create_tags(
            Resources=[subnet_id],
            Tags=[
                {
                    "Key": "Name",
                    "Value": subnet_name
                },
            ],
        )
        return subnet_id

    @staticmethod
    def create_or_get_igw(ec2_client, vpc_id):
        igw_id = None
        igw_response = ec2_client.client.describe_internet_gateways(
            Filters=[{
                'Name': 'attachment.vpc-id',
                'Values': [vpc_id]
            }])

        if 'InternetGateways' in igw_response and igw_response['InternetGateways']:
            igw = igw_response['InternetGateways'][0]
            igw_id = igw['InternetGatewayId']
        else:
            response = ec2_client.client.create_internet_gateway()
            pprint(response)
            igw = response.get("InternetGateway")
            igw_id = igw.get("InternetGatewayId")
            response = ec2_client.client.attach_internet_gateway(InternetGatewayId=igw_id,
                                                                 VpcId=vpc_id)
            print("attached")
            pprint(response)
        return igw_id

    @staticmethod
    def create_route_table_with_route(ec2_client, vpc_id, route_table_name, igw_id):
        response = ec2_client.client.create_route_table(VpcId=vpc_id)
        route_table = response.get("RouteTable")
        pprint(route_table)
        route_table_id = route_table.get("RouteTableId")
        print("Route table id", route_table_id)
        time.sleep(2)
        ec2_client.client.create_tags(
            Resources=[route_table_id],
            Tags=[
                {
                    "Key": "Name",
                    "Value": route_table_name
                },
            ],
        )
        response = ec2_client.client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id,
            RouteTableId=route_table_id,
        )
        return route_table_id

    @staticmethod
    def associate_route_table_to_subnet(ec2_client, route_table_id, subnet_id):
        response = ec2_client.client.associate_route_table(RouteTableId=route_table_id,
                                                           SubnetId=subnet_id)
        print("Route table associated")
        pprint(response)

    @staticmethod
    def enable_auto_public_ips(ec2_client, subnet_id, action):
        new_state = True if action == "enable" else False
        response = ec2_client.client.modify_subnet_attribute(
            MapPublicIpOnLaunch={"Value": new_state}, SubnetId=subnet_id)
        print("Public IP association state changed to", new_state)

    @staticmethod
    def create_route_table_without_route(ec2_client, vpc_id):
        response = ec2_client.client.create_route_table(VpcId=vpc_id)
        route_table = response.get("RouteTable")
        pprint(route_table)
        route_table_id = route_table.get("RouteTableId")
        print("Route table id", route_table_id)
        time.sleep(2)
        ec2_client.client.create_tags(
            Resources=[route_table_id],
            Tags=[
                {
                    "Key": "Name",
                    "Value": "private-route-table"
                },
            ],
        )
        return route_table_id

    @classmethod
    def full_self_create(cls, ec2_client, tag, quantity):
        if quantity > 200:
            print("Too many subnets, aborting")
            LOGGER.error("Too many subnets, aborting")
            return
        vpc_id = cls.create_vpc(ec2_client)
        time.sleep(3)
        cls.add_name_tag(ec2_client, vpc_id, tag)
        # create private and public
        for i in range(1, quantity):
            subnet_id = cls.create_subnet(ec2_client, vpc_id, f'10.22.{i}.0/24',
                                          f'private_sub_{i}')
            rtb_id = cls.create_route_table_without_route(ec2_client, vpc_id)
            time.sleep(2)
            cls.associate_route_table_to_subnet(ec2_client, rtb_id, subnet_id)

            subnet_id = cls.create_subnet(
                ec2_client, vpc_id, f'10.22.{quantity}.0/24',
                f'public_sub_{quantity}')
            rtb_id = cls.create_route_table_with_route(ec2_client, vpc_id, 'my_public_route',
                                                       cls.create_or_get_igw(vpc_id))
            time.sleep(2)
            cls.associate_route_table_to_subnet(ec2_client, rtb_id, subnet_id)
            cls.enable_auto_public_ips(ec2_client, subnet_id, 'enable')

from aws_cdk import (aws_ec2 as ec2, Stack)
from constructs import Construct


class vpcprojectstack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc(
        self, "Webserver_Vpc",
        cidr="10.10.10.0/24",
        max_azs=2,
        nat_gateways=0,
        subnet_configuration=[
            ec2.SubnetConfiguration(name="public", cidr_mask=26, subnet_type=ec2.SubnetType.PUBLIC),
            # ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE)
        ]
    )  
    # Tag all VPC resources
        # Tag.add(vpc,key="Owner",value="Webserver",include_resource_types=[])
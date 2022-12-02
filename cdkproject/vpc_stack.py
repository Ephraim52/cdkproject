from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class CustomVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html
        WebVPC = ec2.Vpc(
                self, "Webserver VPC",
                cidr="10.10.10.0/24",
                availability_zones=["eu-west-2a", "eu-west-2b"],
                nat_gateways=0,
                subnet_configuration=[
                    ec2.SubnetConfiguration(name="public", cidr_mask=25, subnet_type=ec2.SubnetType.PUBLIC),
                    # ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE)
                ]
            )

        AdminVPC = ec2.Vpc(
                self, "Management VPC",
                cidr="10.20.20.0/24",
                availability_zones=["eu-west-2a", "eu-west-2b"],
                nat_gateways=0,
                subnet_configuration=[
                    ec2.SubnetConfiguration(name="public", cidr_mask=25, subnet_type=ec2.SubnetType.PUBLIC),
                    # ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE)
                ]
            )
        
        # Tag all VPC Resources
        # core.Tag.add(vpc,key="Owner",value="Dominic",include_resource_types=[])

        network_acl_props = ec2.NetworkAcl(
            self, "Webserver-ACL",
            vpc= WebVPC,

            # the properties below are optional
            network_acl_name="Webserver ACL",
            subnet_selection=ec2.SubnetSelection(
                availability_zones=["eu-west-2a", "eu-west-2b"],
                one_per_az=False,
                subnet_filters=[ec2.SubnetFilter],
                subnet_group_name="subnetGroupName",
                subnets=[ec2.Subnet],
            )
        )

        network_acl_entry = ec2.NetworkAclEntry(self, "Public Webserver",
            cidr= ec2.AclCidr.any_ipv4(),
            network_acl= ec2.NetworkAcl,
            rule_number=100,
            traffic= ec2.AclTraffic,

            # the properties below are optional
            direction=ec2.TrafficDirection.EGRESS,
            network_acl_entry_name="Public Webserver",
            rule_action=ec2.Action.ALLOW
            
        )

        network_acl_entry = ec2.NetworkAclEntry(self, "Public Webserver",
            cidr= ec2.AclCidr,
            network_acl= ec2.NetworkAcl,
            rule_number=100,
            traffic= ec2.AclTraffic,

            # the properties below are optional
            direction=ec2.TrafficDirection.INGRESS,
            network_acl_entry_name="Public Webserver",
            rule_action=ec2.Action.ALLOW
            
        )

        networkaclprops = ec2.NetworkAcl(
            self, "Admin-server-ACL",
            vpc= AdminVPC,

            # the properties below are optional
            network_acl_name="Admin server ACL",
            subnet_selection=ec2.SubnetSelection(
                availability_zones=["eu-west-2a", "eu-west-2b"],
                one_per_az=False,
                subnet_filters=[ec2.SubnetFilter],
                subnet_group_name="subnetGroupName",
                subnets=[ec2.Subnet],
            )
        )
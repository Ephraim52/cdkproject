from aws_cdk import (
    aws_ec2 as ec2,
    Stack
)

from constructs import Construct

class CustomVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html
        WebVPC = ec2.Vpc(
                self, "Webserver VPC",
                cidr="10.10.10.0/24",
                availability_zones=["eu-west-2a", "eu-west-2b"],
                nat_gateways=0,
                subnet_configuration=[
                    ec2.SubnetConfiguration(name="public", cidr_mask=25, subnet_type=ec2.SubnetType.PUBLIC)
                    # ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE)
                ]
            )

        AdminVPC = ec2.Vpc(
                self, "Management VPC",
                cidr="10.20.20.0/24",
                availability_zones=["eu-west-2a", "eu-west-2b"],
                nat_gateways=0,
                subnet_configuration=[
                    ec2.SubnetConfiguration(name="public", cidr_mask=25, subnet_type=ec2.SubnetType.PUBLIC)
                    # ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE)
                ]
            )
        
        # Tag all VPC Resources
        # core.Tag.add(vpc,key="Owner",value="Dominic",include_resource_types=[])

# this is the Webserver ACL which needs to be Public, accessible from the Admin server only through SSH and RDP
        network_acl_props = ec2.NetworkAcl(
            self, "Webserver-ACL",
            vpc= WebVPC,

            # the properties below are optional
            network_acl_name="Webserver ACL",
            subnet_selection=ec2.SubnetSelection(
                availability_zones=["eu-west-2a", "eu-west-2b"],
                one_per_az=False,
                subnet_type=ec2.SubnetType.PUBLIC
            )
        )
        # these are the entries that specify the rules on what is allowed like, inbound and outbound traffic
        network_acl_entry = ec2.NetworkAclEntry(self, "AllowAllEgress",
            # the CIDR range to allow or deny the subnet access
            cidr= ec2.AclCidr.any_ipv4(),
            network_acl= network_acl_props,
            # rule number represents the protocol rule number
            rule_number=100,
            # What kind of traffic
            traffic= ec2.AclTraffic.tcp_port(80),

            # the properties below are optional
            # Inbound or outbound traffic direction
            direction=ec2.TrafficDirection.EGRESS,
            # key-value with acl rule name
            network_acl_entry_name="AllowAllEgress",
            # whether the rule allows or denies the access that is specified
            rule_action=ec2.Action.ALLOW
            
        )

        networkaclentry = ec2.NetworkAclEntry(self, "AllowAllIngress",
            cidr= ec2.AclCidr.any_ipv4(),
            network_acl= network_acl_props,
            rule_number=100,
            traffic= ec2.AclTraffic.tcp_port(80),

            # the properties below are optional
            direction=ec2.TrafficDirection.INGRESS,
            network_acl_entry_name="AllowAllIngress",
            rule_action=ec2.Action.ALLOW
            
        )
# this is the part of the Admin server ACL which needs to be only accessible with a trusted IP address. 
# from the Admin server access can be established to the Webserver only through SSH and RDP
        AdminACL = ec2.NetworkAcl(
            self, "Admin-server-ACL",
            vpc= AdminVPC,

            # the properties below are optional
            network_acl_name="Admin server ACL",
            subnet_selection=ec2.SubnetSelection(
                availability_zones=["eu-west-2a", "eu-west-2b"],
                one_per_az=False,
                subnet_type=ec2.SubnetType.PUBLIC
            )
        )
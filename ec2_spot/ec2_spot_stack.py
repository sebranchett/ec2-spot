from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class Ec2SpotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc_spot = ec2.Vpc(self, "VPC-spot",
                           nat_gateways=0,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="private",
                                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                                   )
                               ]
                           )

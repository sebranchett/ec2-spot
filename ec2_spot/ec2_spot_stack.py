# from base64 import b64encode, decode
from aws_cdk import (
    # Duration,
    Stack,
    CfnTag,
    aws_ec2 as ec2,
)
from constructs import Construct

# Set Up
# amazon/Deep Learning Base AMI (Amazon Linux) Version 31.1
# in Frankfurt, found using:
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html#finding-an-ami-aws-cli
my_ami = "ami-03ab7bf8ed4e51280"
my_instance_type = "t2.small"
my_max_spot_price = "0.02"
my_tags = [ec2.CfnSpotFleet.SpotFleetTagSpecificationProperty(
    resource_type="instance",
    tags=[CfnTag(key="Creator", value="SEB")]
    )]
# byte_data = open("./user_data/user_data.sh", "rb").read()
# my_user_data = b64encode(byte_data).decode()


class Ec2SpotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iamFleetRole = "arn:aws:iam::" + \
                       self.account + \
                       ":role/aws-ec2-spot-fleet-tagging-role"

        # VPC
        my_vpc = ec2.Vpc(self, "VPC-spot",
                         nat_gateways=0,
                         subnet_configuration=[
                             ec2.SubnetConfiguration(
                                 name="private",
                                 subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                                 )
                             ]
                         )
        my_subnets = my_vpc.select_subnets().subnet_ids
        print(my_subnets)
        # Spot fleet
        # If you specify LaunchSpecifications,
        # you can’t specify LaunchTemplateConfigs
        # launch_specs = \
        #     [ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
        #                 image_id="ami-03ab7bf8ed4e51280",
        #                 instance_type="t2.medium",
        #                 ),
        #                 ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
        #                 image_id="ami-03ab7bf8ed4e51280",
        #                 instance_type="t2.small",
        #                 ),
        #                 ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
        #                 image_id="ami-03ab7bf8ed4e51280",
        #                 instance_type="m3.medium",
        #                 ),
        #                 ]
        #                 # tag_specifications=my_tags,
        #                 # user_data=my_user_data

        config_data = \
            ec2.CfnSpotFleet.SpotFleetRequestConfigDataProperty(
                allocation_strategy="capacityOptimized",
                iam_fleet_role=iamFleetRole,
                spot_price="0.08",
                target_capacity=1,
                terminate_instances_with_expiration=True,
                type="request",
                launch_specifications=[
                    ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
                        image_id="ami-03ab7bf8ed4e51280",
                        instance_type="t2.medium",
                        subnet_id=my_subnets[0],
                    ),
                    ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
                        image_id="ami-03ab7bf8ed4e51280",
                        instance_type="t2.small",
                        subnet_id=my_subnets[0],
                    ),
                    ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
                        image_id="ami-03ab7bf8ed4e51280",
                        instance_type="m3.medium",
                        subnet_id=my_subnets[0],
                    ),
                    ]
                )

        ec2.CfnSpotFleet(
                        self, "MyCfnSpotFleet",
                        spot_fleet_request_config_data=config_data
                        )

from aws_cdk import (
    # Duration,
    Stack,
    CfnTag,
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

        # Spot fleet
        iamFleetRole = "arn:aws:iam::" + \
                       self.account + \
                       ":role/aws-ec2-spot-fleet-tagging-role"

        # Deep Learning Base AMI (Ubuntami-02u 18.04) Version 50.0 in Frankfurt
        my_ami = "ami-03ab7bf8ed4e51280"
        my_instance_type = ec2.InstanceType("t2.small")
        max_spot_price = "0.02"
        # Always tag
        my_tags = ec2.CfnSpotFleet.SpotFleetTagSpecificationProperty(
            resource_type="resourceType",
            tags=[CfnTag(key="Creator", value="SEB")]
            )

        # If you specify LaunchSpecifications,
        # you can’t specify LaunchTemplateConfigs
        launch_specs = ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty(
                        image_id=my_ami,
                        )
                        # instance_type=my_instance_type,
                        # spot_price=max_spot_price,
                        # tag_specifications=my_tags
#                        user_data=
#                        subnet_id=

        config_data = ec2.CfnSpotFleet.SpotFleetRequestConfigDataProperty(
                        iam_fleet_role=iamFleetRole,
                        target_capacity=1,
                        launch_specifications=launch_specs,
                        on_demand_target_capacity=0,
                        spot_price=max_spot_price,
                        type="request"
                        )

        spot_fleet = ec2.CfnSpotFleet(
                        self, "MyCfnSpotFleet",
                        spot_fleet_request_config_data=config_data
                        )

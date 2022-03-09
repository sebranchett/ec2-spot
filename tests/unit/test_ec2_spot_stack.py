import aws_cdk as core
import aws_cdk.assertions as assertions

from ec2_spot.ec2_spot_stack import Ec2SpotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ec2_spot/ec2_spot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Ec2SpotStack(app, "ec2-spot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

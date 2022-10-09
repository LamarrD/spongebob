import aws_cdk as core
import aws_cdk.assertions as assertions

from spongebob.spongebob_stack import SpongebobStack

# example tests. To run these tests, uncomment this file along with the example
# resource in spongebob/spongebob_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SpongebobStack(app, "spongebob")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

from constructs import Construct
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)

from consts import CLOUDFRONT_IPS


class BackendStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Dynamo Table
        table = dynamodb.Table(
            self,
            "spongebob",
            partition_key=dynamodb.Attribute(
                name="pk", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # API Gateway
        api_resource_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["execute-api:Invoke"],
                    principals=[iam.StarPrincipal()],
                    resources=["execute-api:/*/*/*"],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.DENY,
                    principals=[iam.StarPrincipal()],
                    actions=["execute-api:Invoke"],
                    resources=["execute-api:/*/*/*"],
                    conditions={"NotIpAddress": {"aws:SourceIp": CLOUDFRONT_IPS}},
                ),
            ]
        )

        api = apigateway.RestApi(
            self,
            "spongebob-api",
            policy=api_resource_policy,
        )
        characters = api.root.add_resource("characters")
        character = api.root.add_resource("character").add_resource("{character}")

        # Lambdas
        characters_list = create_function(
            self, "characters_list", table, "GET", characters
        )
        character_get = create_function(self, "character_get", table, "GET", character)

        # Create a cfn output for the API Gateway URL
        cdk.CfnOutput(self, "API URL", value=api.url)


def create_function(self, name, table, method, root):
    """Helper function to create a lambda function and add it to the API Gateway."""
    lambda_function = lambda_.Function(
        self,
        name,
        code=lambda_.Code.from_asset("../functions/"),
        runtime=lambda_.Runtime.PYTHON_3_8,
        handler=f"{name}.handler",
        environment={"TABLE_NAME": table.table_name},
    )
    table.grant_read_data(lambda_function)
    lambda_function_integration = apigateway.LambdaIntegration(lambda_function)
    root.add_method(method, lambda_function_integration)

from unicodedata import name
from constructs import Construct
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
)

class SpongebobStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Dynamo Table
        table = dynamodb.Table(self, "spongebob",
            partition_key=dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Lambdas
        characters_list = lambda_.Function(self, "character-list",
            code=lambda_.Code.from_asset('./src'),
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="character_list.handler",
            environment={
                "TABLE_NAME": table.table_name
            }
        )
        table.grant_read_data(characters_list)

        characters_get = lambda_.Function(self, "character-get",
            code=lambda_.Code.from_asset('./src'),
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="character_get.handler",
            environment={
                "TABLE_NAME": table.table_name
            }
        )
        table.grant_read_data(characters_get)

        # API Gateway
        api = apigateway.RestApi(self, "spongebob-api")
        characters = api.root.add_resource("characters")
        characters_list_integration = apigateway.LambdaIntegration(characters_list)
        characters.add_method("GET", characters_list_integration)

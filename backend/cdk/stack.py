from constructs import Construct
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_s3 as s3,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_ssm as ssm,
    aws_events as events,
    aws_events_targets as targets,
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
        api = apigateway.RestApi(
            self,
            "spongebob-api",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS
            )
        )
        characters = api.root.add_resource("characters")
        character = api.root.add_resource("character").add_resource("{character}")
        character_fact = character.add_resource("fact")

        # Create lambda layer
        layer = lambda_.LayerVersion(
            self,
            "headless-chrome-layer",
            code=lambda_.Code.from_asset("../tests/canaries/layer-headless-chrome.zip"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
        )

        # Lambdas
        characters_list = create_function( self, "characters_list", table, "GET", characters )
        character_get = create_function(self, "character_get", table, "GET", character)
        character_put = create_function(self, "character_put", table, "PUT", character)
        character_fact_get = create_function(self, "character_fact_get", table, "GET", character_fact)
        character_fact_get.add_layers(
        )

        table.grant_read_write_data(character_put)

        # S3 buckets for canary screenshots
        canary_bucket = s3.Bucket( self, "canary-screenshots")


        # Canary Alarms and SNS topic
        canary_topic = sns.Topic(self, "canary-topic")
        canary_topic.add_subscription(sns_subscriptions.UrlSubscription(
            ssm.StringParameter.value_for_string_parameter(self, "pd-url"), protocol=sns.SubscriptionProtocol.HTTPS
        ))

        # Canaries
        characters_canary = create_canary_function( self, "characters", layer, canary_bucket, canary_topic )
        home_canary = create_canary_function( self, "home", layer, canary_bucket, canary_topic)

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
        timeout=cdk.Duration.seconds(30),
    )
    table.grant_read_data(lambda_function)
    lambda_function_integration = apigateway.LambdaIntegration(lambda_function)
    root.add_method(method, lambda_function_integration)
    return lambda_function


def create_canary_function(self, name, layer, canary_bucket, canary_topic):
    """Helper function to create a canaries and setup alarms"""
    canary = lambda_.Function(
        self,
        f"{name}_canary",
        code=lambda_.Code.from_asset("../tests/canaries/e2e/", exclude=["headless_chrome.py"]),
        timeout=cdk.Duration.seconds(120),
        handler=f"{name}.handler",
        runtime=lambda_.Runtime.PYTHON_3_8,
        layers=[layer],
        memory_size=1024,
        environment={"S3_BUCKET": canary_bucket.bucket_name},
    )
    events.Rule(
        self,
        f"{name}_canary_alarm",
        schedule=events.Schedule.expression("rate(1 day)"),
        targets=[targets.LambdaFunction(canary)],
    )
    canary_bucket.grant_read_write( canary )
    canary_alarm = cloudwatch.Alarm(
        self,
        f"{name}_alarm",
        metric=canary.metric_errors(),
        threshold=1,
        evaluation_periods=1,
        treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
    )
    canary_alarm.add_alarm_action( cloudwatch_actions.SnsAction( topic=canary_topic, ) )
    return canary
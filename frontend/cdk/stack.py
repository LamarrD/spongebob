from constructs import Construct
from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
    Stack,
    CfnOutput,
)


class FrontendStack(Stack):
    """A static website served via S3+CloudFront+Route53."""

    def __init__(
        self, scope: Construct, id: str, domain_name: str, hosted_zone_id: str
    ):
        super().__init__(scope, id)

        # Get a reference to the hosted zone AWS automatically creates when you register a domain
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "hosted-zone", hosted_zone_id=hosted_zone_id, zone_name=domain_name
        )

        # Create a certificate for the domain
        certificate = acm.Certificate(
            self,
            "certificate",
            domain_name=domain_name,
            subject_alternative_names=[f"*.{domain_name}"],
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # Create a plain bucket for the website to be hosted out of, note we do not name it or make it public
        site_bucket = s3.Bucket(self, "site-bucket")

        # Create a CloudFront distribution to sit in front of the bucket and actually serve the content
        distribution = cloudfront.Distribution(
            self,
            "distribution",
            certificate=certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(site_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
            domain_names=[domain_name],
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                )
            ],
        )

        # Create an A record in Route53 so the CloudFront distribution can be accessed via the domain name
        route53.ARecord(
            self,
            "alias-record",
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
            zone=hosted_zone,
            record_name=domain_name,
        )

        # Create an output of the s3 bucket name so we can reference it when we deploy the frontend content to it
        CfnOutput(self, "bucket-name", value=site_bucket.bucket_name)
        CfnOutput(self, "distribution-id", value=distribution.distribution_id)
        CfnOutput(self, "certificate-arn", value=certificate.certificate_arn)

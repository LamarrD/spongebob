#!/usr/bin/env python3
import aws_cdk as cdk
from stack import FrontendStack


app = cdk.App()
FrontendStack(app, "Spongebob-Frontend", domain_name = "myleg.org", hosted_zone_id='Z09617661EI2TT6NVT61R')
app.synth()
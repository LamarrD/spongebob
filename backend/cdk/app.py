#!/usr/bin/env python3
import aws_cdk as cdk
from stack import BackendStack


app = cdk.App()
BackendStack(app, "Spongebob-Backend", hosted_zone_id='Z09617661EI2TT6NVT61R')
app.synth()

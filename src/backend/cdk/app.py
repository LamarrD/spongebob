#!/usr/bin/env python3
import aws_cdk as cdk
from spongebob_stack import SpongebobStack


app = cdk.App()
SpongebobStack(app, "SpongebobStack",)

app.synth()

#!/usr/bin/env python3
import aws_cdk as cdk
from stack import BackendStack


app = cdk.App()
BackendStack(app, "Spongebob-Backend")
app.synth()

#!/usr/bin/env python3

import aws_cdk as cdk

from cdkproject.cdkproject_stack import CdkprojectStack


app = cdk.App()
CdkprojectStack(app, "cdkproject")

app.synth()

#!/usr/bin/env python3

import aws_cdk as cdk

from cdkproject.vpc_stack import CustomVpcStack


app = cdk.App()
CustomVpcStack(app, "cdkproject")

app.synth()

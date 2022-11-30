#!/usr/bin/env python3

import aws_cdk as cdk

from cdkproject.vpc_project_stack import vpcprojectstack


app = cdk.App()
vpcprojectstack(app, "cdkproject-vpc-stack")

app.synth()

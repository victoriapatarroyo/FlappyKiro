#!/usr/bin/env python3
"""CDK App — Flappy Kiro Web Hosting."""
import aws_cdk as cdk
from stacks.hosting_stack import FlappyKiroHostingStack

app = cdk.App()

FlappyKiroHostingStack(
    app,
    "FlappyKiroHostingStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1",
    ),
)

app.synth()

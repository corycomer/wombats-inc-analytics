#!/usr/bin/env python3
from aws_cdk import core
from stacks.analytics_stack import AnalyticsStack
from stacks.redshift_stack import RedshiftStack
from stacks.glue_stack import GlueStack  # New import for GlueStack

app = core.App()

# Deploy RedshiftStack
redshift_stack = RedshiftStack(app, "RedshiftStack")

# Deploy AnalyticsStack and pass in the S3 bucket from AnalyticsStack
analytics_stack = AnalyticsStack(
    app, "AnalyticsStack", redshift_cluster=redshift_stack.cluster
)

# Deploy GlueStack and pass the S3 bucket from AnalyticsStack
glue_stack = GlueStack(
    app, "GlueStack", s3_bucket=analytics_stack.bucket
)

app.synth()

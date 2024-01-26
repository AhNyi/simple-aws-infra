#!/usr/bin/env python3
import os

import aws_cdk as core

from simple_aws_infra.dynamodb_stack import DynamodbStack
from simple_aws_infra.simple_stack import SimpleStack


app = core.App()

stage = app.node.try_get_context("stage")
stage_params = app.node.try_get_context("stages")[stage]

dynamodb_stack = DynamodbStack(
    app,
    "simple-dynamodb",
    table_name=stage_params["dynamodb_table_name"],
    autoscale_min_read_capacity=5,
    autoscale_max_read_capacity=10000,
    autoscale_min_write_capacity=5,
    autoscale_max_write_capacity=10000,
    env={"region": stage_params["region"], "account": stage_params["account"]},
)

SimpleStack(app, "simple-default",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

# for key, value in tags.items():
#    core.Tags.of(app).add(key, value)

app.synth()

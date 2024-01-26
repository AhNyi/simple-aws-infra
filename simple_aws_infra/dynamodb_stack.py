from aws_cdk import (
    aws_dynamodb as dynamodb,
    Stack,
    aws_iam as iam,
)

from typing import Optional
from constructs import Construct

import aws_cdk as core

class DynamodbStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        table_name: str,
        autoscale_min_read_capacity: int,
        autoscale_max_read_capacity: int,
        autoscale_min_write_capacity: int,
        autoscale_max_write_capacity: int,
        **kwargs,        
    ) -> None:
        super().__init__(scope, id, **kwargs)
        
        # ##########
        # Parameters
        # ##########
        
        param_autoscale_min_read_capacity = core.CfnParameter(
            self,
            "AutoscaleMinReadCapacity",
            description="autoscale min read capacity",
            type="Number",
            min_value=1,
            default=autoscale_min_read_capacity,
        )
        
        param_autoscale_max_read_capacity = core.CfnParameter(
            self,
            "AutoscaleMaxReadCapacity",
            description="autoscale max read capacity",
            type="Number",
            min_value=1,
            default=autoscale_max_read_capacity,
        )
        
        param_autoscale_min_write_capacity = core.CfnParameter(
            self,
            "AutoscaleMinWriteCapacity",
            description="autoscale min write capacity",
            type="Number",
            min_value=1,
            default=autoscale_min_write_capacity,
        )
        
        param_autoscale_max_write_capacity = core.CfnParameter(
            self,
            "AutoscaleMaxWriteCapacity",
            description="autoscale max write capacity",
            type="Number",
            min_value=1,
            default=autoscale_max_write_capacity,
        )
        
        # ##########
        # Resources
        # ##########
        
        # table
        self.table = dynamodb.Table(
            self,
            "Table",
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name="ID",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="ItemType",
                type=dynamodb.AttributeType.STRING,
            ),
            read_capacity=param_autoscale_min_read_capacity.value_as_number,
            write_capacity=param_autoscale_min_write_capacity.value_as_number,
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            encryption=dynamodb.TableEncryption.AWS_MANAGED,
            point_in_time_recovery=True,
            time_to_live_attribute="Ttl",
        )
        self.table.auto_scale_read_capacity(
            min_capacity=param_autoscale_min_read_capacity.value_as_number,
            max_capacity=param_autoscale_max_read_capacity.value_as_number,
        ).scale_on_utilization(target_utilization_percent=70)
        self.table.auto_scale_write_capacity(
            min_capacity=param_autoscale_min_write_capacity.value_as_number,
            max_capacity=param_autoscale_max_write_capacity.value_as_number,
        ).scale_on_utilization(target_utilization_percent=70)
        
        # index settings
        self._setup_autoscale_gsi(
            table=self.table,
            partition_key="ContractID",
            sort_key="ItemType",
            autoscale_min_read_capacity=autoscale_min_read_capacity,
            autoscale_max_read_capacity=autoscale_max_read_capacity,
            autoscale_min_write_capacity=autoscale_min_write_capacity,
            autoscale_max_write_capacity=autoscale_max_write_capacity,
        )
        
        # policies
        write_policy = iam.ManagedPolicy(
            self,
            "simpleInfraDynamodbWritePolicy",
            managed_policy_name="simpleInfraDynamodbWritePolicy",
            document=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["dynamodb:*"],
                        resources=[self.table.table_arn],
                    ),
                ],
            ),
        )
        
        read_policy = iam.ManagedPolicy(
            self,
            "simpleInfraDynamodbReadPolicy",
            managed_policy_name="simpleInfraDynamodbReadPolicy",
            document=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "dynamodb:BatchGetItem",
                            "dynamodb:Describe*",
                            "dynamodb:List*",
                            "dynamodb:GetItem",
                            "dynamodb:Query",
                            "dynamodb:Scan",
                        ],
                        resources=[self.table.table_arn],
                    ),
                ],
            ),
        )
        
        # #######
        # Outputs
        # #######
        
        core.CfnOutput(
            self,
            "simpleInfraDynamodbReadPolicyName",
            value=read_policy.managed_policy_name,
            export_name="simpleInfraDynamodbReadPolicy",
        )
        core.CfnOutput(
            self,
            "simpleInfraDynamodbWritePolicyName",
            value=write_policy.managed_policy_name,
            export_name="simpleInfraDynamodbWritePolicy",
        )
        core.CfnOutput(
            self,
            "TableName",
            value=self.table.table_name,
            description="simpleInfra Table",
            export_name="simpleInfraTable",
        )
        
    def _setup_autoscale_gsi(
        self,
        table: dynamodb.Table,
        partition_key: str,
        sort_key: Optional[str] = None,
        partition_key_type: dynamodb.AttributeType = dynamodb.AttributeType.STRING,
        sort_key_type: dynamodb.AttributeType = dynamodb.AttributeType.STRING,
        autoscale_min_read_capacity: int = 5,
        autoscale_max_read_capacity: int = 10000,
        autoscale_min_write_capacity: int = 5,
        autoscale_max_write_capacity: int = 10000,
    ):
        index_name = (
            f"{partition_key}-{sort_key}-index"
            if sort_key 
            else f"{partition_key}-index"
        )
        
        param_autoscale_min_read_capacity = core.CfnParameter(
            self,
            f"{index_name}_AutoscaleMinReadCapacity",
            description=f"{index_name} autoscale min read capacity",
            type="Number",
            min_value=1,
            default=autoscale_min_read_capacity,
        )
        param_autoscale_max_read_capacity = core.CfnParameter(
            self,
            f"{index_name}_AutoscaleMaxReadCapacity",
            description=f"{index_name} autoscale max read capacity",
            type="Number",
            min_value=1,
            default=autoscale_max_read_capacity,
        )
        param_autoscale_min_write_capacity = core.CfnParameter(
            self,
            f"{index_name}_AutoscaleMinWriteCapacity",
            description=f"{index_name} autoscale min write capacity",
            type="Number",
            min_value=1,
            default=autoscale_min_write_capacity,
        )
        param_autoscale_max_write_capacity = core.CfnParameter(
            self,
            f"{index_name}_AutoscaleMaxWriteCapacity",
            description=f"{index_name} autoscale max write capacity",
            type="Number",
            min_value=1,
            default=autoscale_max_write_capacity,
        )
        
        index_options = {
            "index_name": index_name,
            "partition_key": dynamodb.Attribute(
                name=partition_key,
                type=partition_key_type,
            ),
            "read_capacity": param_autoscale_min_read_capacity.value_as_number,
            "write_capacity": param_autoscale_min_write_capacity.value_as_number,
        }
        if sort_key:
            index_options["sort_key"] = dynamodb.Attribute(
                name=sort_key,
                type=sort_key_type,
            )
        table.add_global_secondary_index(**index_options)
        
        table.auto_scale_global_secondary_index_read_capacity(
            index_name=index_name,
            min_capacity=param_autoscale_min_read_capacity.value_as_number,
            max_capacity=param_autoscale_max_read_capacity.value_as_number,
        ).scale_on_utilization(target_utilization_percent=70)
        table.auto_scale_global_secondary_index_write_capacity(
            index_name=index_name,
            min_capacity=param_autoscale_min_write_capacity.value_as_number,
            max_capacity=param_autoscale_max_write_capacity.value_as_number,
        ).scale_on_utilization(target_utilization_percent=70)
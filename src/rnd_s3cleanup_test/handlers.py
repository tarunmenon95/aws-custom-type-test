import logging
from statistics import mode
import time
import boto3
import json

from typing import Any, MutableMapping, Optional
from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)
from .models import ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "rnd::s3cleanup::test"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint

@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    try:
        create_lambda_function(model.Runtime)
        # Setting Status to success will signal to cfn that the operation is complete
        progress.status = OperationStatus.SUCCESS
        progress.resourceModel = model
        return progress
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        progress.status = OperationStatus.FAILED
        progress.message=f"Create failed with {e} ---"
        progress.errorCode=HandlerErrorCode.InternalFailure
        return progress
    


# @resource.handler(Action.UPDATE)
# def update_handler(
#     session: Optional[SessionProxy],
#     request: ResourceHandlerRequest,
#     callback_context: MutableMapping[str, Any],
# ) -> ProgressEvent:
#     model = request.desiredResourceState
#     progress: ProgressEvent = ProgressEvent(
#         status=OperationStatus.IN_PROGRESS,
#         resourceModel=model,
#     )
#     # TODO: put code here
#     return progress


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )
    try:
        lambda_client = boto3.client("lambda")
        lambda_client.delete_function(
            FunctionName="s3-cleaner-function"
        )
        progress.status = OperationStatus.SUCCESS
        progress.resourceModel = model
        return progress
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        progress.status = OperationStatus.FAILED
        progress.message=f"Create failed with {e} ---"
        progress.errorCode=HandlerErrorCode.InternalFailure
        return progress

@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


# @resource.handler(Action.LIST)
# def list_handler(
#     session: Optional[SessionProxy],
#     request: ResourceHandlerRequest,
#     callback_context: MutableMapping[str, Any],
# ) -> ProgressEvent:
#     # TODO: put code here
#     return ProgressEvent(
#         status=OperationStatus.SUCCESS,
#         resourceModels=[],
#     )


def create_lambda_function(runtime):
    lambda_client = boto3.client("lambda")
    iam_client = boto3.client("iam")

    #Assume Role Document
    assume_role_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
            }
        ]
    })

    #IAM Policy for lambda function
    managed_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:Get*",
                    "s3:List*"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    })
    try:
        #Policy ARN
        iam_policy_arn = iam_client.create_policy(
        PolicyName='s3-cleaner-policy',
        PolicyDocument=managed_policy
        )["Policy"]["Arn"]
    except Exception as e:
        print(e)

    try:
        #IAM Role
        iam_role_arn = iam_client.create_role(
            RoleName="S3CleanerRole",
            AssumeRolePolicyDocument=assume_role_document
        )["Role"]["Arn"]
    except Exception as e:
        print(e)
        
        #Attach policy to role
        iam_client.attach_role_policy(
            PolicyArn=iam_policy_arn,
            RoleName="S3CleanerRole",
        )

    print(iam_role_arn)
    time.sleep(30)

    #Create lambda function with role
    resp = lambda_client.create_function(
        FunctionName="s3-cleaner-function",
        Role=iam_role_arn,
        Runtime=runtime,
        Handler="lambda.handler",
        Code={
            "ZipFile": open('lambda.zip', 'rb').read()
        }
    )
    
    return resp

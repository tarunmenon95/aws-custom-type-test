from .documents import ASSUME_ROLE_DOCUMENT, MANAGED_POLICY_DOCUMENT
from cloudformation_cli_python_lib import exceptions
import boto3


class IamResources:
    
    def __init__(self):
        self.ASSUME_ROLE_DOCUMENT = ASSUME_ROLE_DOCUMENT
        self.MANAGED_POLICY_DOCUMENT = MANAGED_POLICY_DOCUMENT
        self.iam_client = boto3.client("iam")
        self.policy_name = "s3-cleaner-policy"

    def create_policy(self):
        try:
            iam_policy_arn = self.iam_client.create_policy(
                PolicyName=self.policy_name,
                PolicyDocument=self.MANAGED_POLICY_DOCUMENT
                )["Policy"]["Arn"]
        except self.iam_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                iam_policy_arn = f"arn:aws:iam::870418506002:policy/{self.policy_name}"
            else:
                raise e
            
        return iam_policy_arn
    
    def create_role(self):
        try:
            #IAM Role
            iam_role_arn = self.iam_client.create_role(
                RoleName="S3CleanerRole",
                AssumeRolePolicyDocument=self.ASSUME_ROLE_DOCUMENT
            )["Role"]["Arn"]
        except self.iam_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                iam_role_arn = "arn:aws:iam::870418506002:role/S3CleanerRole"
                self.iam_client.attach_role_policy(
                PolicyArn=self.create_policy(),
                RoleName="S3CleanerRole",
            )
            else:
                raise e
            
        return iam_role_arn
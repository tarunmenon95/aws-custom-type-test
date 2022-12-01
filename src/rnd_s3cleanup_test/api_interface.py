import logging
import time
from typing import Optional

from cloudformation_cli_python_lib import Resource, SessionProxy, exceptions
from botocore.exceptions import WaiterError, ClientError
from .models import ResourceModel
from .translator import Translator
from .iam_resources import IamResources
import os

LOG = logging.getLogger(__name__)
class ApiInterface:
    def __init__(self, session: Optional[SessionProxy], resource: Resource):
        if session is None or not isinstance(session, SessionProxy):
            raise exceptions.InternalFailure("session should be a SessionProxy")
        self.session = session
        self.client = self.session.client("lambda")
        self.resource = resource
        self.iam_resource = IamResources()

    def read_model(self, model: ResourceModel) -> ResourceModel:
        LOG.info("Reading Model")
        read_request = Translator.translate_model_to_read_request(model)
        waiter = self.client.get_waiter('function_exists')
        try:
            waiter.wait(
                FunctionName=read_request["FunctionName"],
                WaiterConfig={
                    'Delay': 5,
                    'MaxAttempts': 6
                }
            )
            response = self.client.get_function(FunctionName=read_request["FunctionName"])["Configuration"]
            
        except WaiterError as e:
            print("WAITTEEEERRRR")
            raise exceptions.NotFound(
                    "self.resource.type_name",
                    f"{read_request['FunctionName']}",
            )
        except self.client.exceptions.ResourceNotFoundException:
            print("Default RNFE")
            raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{read_request['FunctionName']}",
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("And not found")
                raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{read_request['FunctionName']}",
                )
            else:
                raise exceptions.InternalFailure()
            
        
        
        return Translator.translate_read_response_to_model(response)

    def model_exists(self, model: ResourceModel) -> bool:
        LOG.info("Validating Model Exists")
        try:
            self.read_model(model)
            return True
        except exceptions.NotFound:
            return False

    def create_model(self, model: ResourceModel) -> None:
        LOG.info("Creating Model")
        create_request = Translator.translate_model_to_create_request(model)
        
        file_path = os.path.join('./rnd_s3cleanup_test', 'lambda.zip')
        time.sleep(5)  
        try:
            self.client.create_function(
                FunctionName=create_request["FunctionName"],
                Role=self.iam_resource.create_role(),
                Runtime=create_request["Runtime"],
                Handler="lambda.handler",
                Code={
                    "ZipFile": open(file_path, 'rb').read()
                }
            )
           
        except self.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                raise exceptions.AlreadyExists(str(e), f"{create_request['FunctionName']}")

    def delete_model(self, model: ResourceModel) -> None:
        LOG.info("Deleting Model")
        delete_request = Translator.translate_model_to_delete_request(model)
        try:
            self.client.delete_function(FunctionName=delete_request["FunctionName"])
            #TODO Cleanup IAM Resources aswell....
        except ClientError as e:
            print("Client Errah")
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("And not found")
                raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{delete_request['FunctionName']}",
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            print("Default RNFE")
            raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{delete_request['FunctionName']}",
            )
import time
from typing import Optional

from cloudformation_cli_python_lib import Resource, SessionProxy, exceptions

from .models import ResourceModel
from .translator import Translator
from .iam_resources import IamResources
import os

class ApiInterface:
    def __init__(self, session: Optional[SessionProxy], resource: Resource):
        if session is None or not isinstance(session, SessionProxy):
            raise exceptions.InternalFailure("session should be a SessionProxy")
        self.session = session
        self.client = self.session.client("lambda")
        self.resource = resource
        self.iam_resource = IamResources()

    def read_model(self, model: ResourceModel) -> ResourceModel:
        read_request = Translator.translate_model_to_read_request(model)
        try:
            response = self.client.get_function(FunctionName=read_request["name"])["Configuration"]
        except self.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{read_request['name']}:{read_request['runtime']}",
                )
            else:
                raise e
        return Translator.translate_read_response_to_model(response)

    def model_exists(self, model: ResourceModel) -> bool:
        try:
            self.read_model(model)
            return True
        except exceptions.NotFound:
            return False

    def create_model(self, model: ResourceModel) -> None:
        create_request = Translator.translate_model_to_create_request(model)
        
        file_path = os.path.join('./rnd_s3cleanup_test', 'lambda.zip')
        time.sleep(15)  
        try:
            self.client.create_function(
                FunctionName=create_request["Name"],
                Role=self.iam_resource.create_role(),
                Runtime=create_request["Runtime"],
                Handler="lambda.handler",
                Code={
                    "ZipFile": open(file_path, 'rb').read()
                }
            )
           
        except self.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                raise exceptions.AlreadyExists(str(e), f"{create_request['Name']}")

    def delete_model(self, model: ResourceModel) -> None:
        delete_request = Translator.translate_model_to_delete_request(model)
        try:
            self.client.delete_function(FunctionName=delete_request["name"])
        except self.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{delete_request['name']}",
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise exceptions.NotFound(
                    self.resource.type_name,
                    f"{delete_request['name']}",
            )
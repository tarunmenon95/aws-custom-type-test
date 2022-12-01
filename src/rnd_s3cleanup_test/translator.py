from .models import (
    ResourceModel
)


class Translator:
    @staticmethod
    def translate_model_to_read_request(model: ResourceModel) -> dict:
        request = {
            "FunctionName": model.FunctionName,
            "Runtime": model.Runtime,
            "FunctionArn": model.FunctionArn
        }
        return request

    @staticmethod
    def translate_read_response_to_model(read_response: dict) -> ResourceModel:
        model = ResourceModel(
            FunctionName=read_response.get("FunctionName", None),
            Runtime=read_response.get("Runtime", None),
            FunctionArn=read_response.get("FunctionArn", None)
        )
        return model

    @staticmethod
    def translate_model_to_create_request(model: ResourceModel) -> dict:
        request = {
            "FunctionName": model.FunctionName,
        }
        if model.FunctionName is not None:
            request["FunctionName"] = model.FunctionName
        if model.Runtime is not None:
            request["Runtime"] = model.Runtime
        if model.FunctionArn is not None:
            request["FunctionArn"] = model.FunctionArn

        return request

    @staticmethod
    def translate_model_to_update_request(model: ResourceModel) -> dict:
        return Translator.translate_model_to_create_request(model)

    @staticmethod
    def translate_model_to_delete_request(model: ResourceModel) -> dict:
        request = {
            "FunctionName": model.FunctionName,
        }
        return request

from .models import (
    ResourceModel
)


class Translator:
    @staticmethod
    def translate_model_to_read_request(model: ResourceModel) -> dict:
        request = {
            "name": model.Name,
            "runtime": model.Runtime
        }
        return request

    @staticmethod
    def translate_read_response_to_model(read_response: dict) -> ResourceModel:
        model = ResourceModel(
            Name=read_response.get("FunctionName", None),
            Runtime=read_response.get("Runtime", None),
        )
        return model

    @staticmethod
    def translate_model_to_create_request(model: ResourceModel) -> dict:
        request = {
            "name": model.Name,
        }
        if model.Name is not None:
            request["Name"] = model.Name
        if model.Runtime is not None:
            request["Runtime"] = model.Runtime

        return request

    @staticmethod
    def translate_model_to_update_request(model: ResourceModel) -> dict:
        return Translator.translate_model_to_create_request(model)

    @staticmethod
    def translate_model_to_delete_request(model: ResourceModel) -> dict:
        request = {
            "name": model.Name,
        }
        return request

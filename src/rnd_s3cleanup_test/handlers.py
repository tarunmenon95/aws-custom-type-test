import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
)

from .api_interface import ApiInterface
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
    LOG.info(str(request))
    requested_model = request.desiredResourceState
    if requested_model is None or requested_model.Name is None:
        raise exceptions.InvalidRequest("Name property is a required field")
    api_interface = ApiInterface(session, resource)
    if api_interface.model_exists(requested_model):
        raise exceptions.AlreadyExists(resource.type_name, f"{requested_model.Name}")
    api_interface.create_model(requested_model)
    LOG.info("Lambda created")
    return read_handler(session, request, callback_context)

@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    _: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info(str(request))
    requested_model = request.desiredResourceState
    if requested_model is None or requested_model.Name is None:
        raise exceptions.InvalidRequest("Name property is a required field")
    api_interface = ApiInterface(session, resource)
    api_interface.delete_model(requested_model)
    LOG.info("Lambda deleted")
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
    )

@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    _: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info(str(request))
    requested_model = request.desiredResourceState
    if requested_model is None or requested_model.Name is None:
        raise exceptions.InvalidRequest("Name property is a required field")
    api_interface = ApiInterface(session, resource)
    response_model = api_interface.read_model(requested_model)
    LOG.info("Lambda found")
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=response_model,
    )

import json

from indra.agent import AgentEncoder
from registry.execution_registry import CLI_EXEC_KEY

ERROR = "Error:"

ENDPOINT_DESCR = "Put to this endpoint to "


def err_return(s):
    return {ERROR: s}


def json_converter(obj, execution_key=CLI_EXEC_KEY):
    json_object = json.loads(json.dumps(obj.to_json(),
                                        cls=AgentEncoder, indent=4))

    if execution_key is not None:
        json_object["execution_key"] = execution_key

    return json_object

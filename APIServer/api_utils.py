import json

from indra.agent import AgentEncoder

ERROR = "Error:"


def err_return(s):
    return {ERROR: s}


def json_converter(obj):
    return json.loads(json.dumps(obj.to_json(),
                                 cls=AgentEncoder, indent=4))

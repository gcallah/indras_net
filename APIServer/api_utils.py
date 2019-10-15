import json
from indra.agent import AgentEncoder


def json_converter(object):
    return json.loads(json.dumps(object.to_json(),
                      cls=AgentEncoder, indent=4))

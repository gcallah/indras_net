from registry import registry
from numpy import random
from propargs.constants import *

BILLION = 10 ** 9

COMMANDLINE_EXECUTION_KEY = 0
# establish shorter var name:
CLI_EXEC_KEY = COMMANDLINE_EXECUTION_KEY

EXECUTION_KEY_NAME = "execution_key"
EXEC_KEY_NM = EXECUTION_KEY_NAME


def init_exec_key(props=None):
    return int(props[EXEC_KEY_NM].val) if props is not None else CLI_EXEC_KEY


class ExecutionRegistry(object):
    def __init__(self):
        self.registries = {}
        self.registries[COMMANDLINE_EXECUTION_KEY] = {}

    def get_unique_key(self):
        key = random.randint(1, BILLION)
        return key

    def register(self, agent_registry: registry):
        key = self.get_unique_key()
        self.registries[key] = agent_registry

    def create_new_execution_registry(self):
        key = self.get_unique_key()
        self.registries[key] = {}
        return key

    def __set_value_at_key(self, key=COMMANDLINE_EXECUTION_KEY, value=None,
                           object_to_register=None):
        if isinstance(key, str):
            key = int(key)
        self.does_key_exists(key)
        self.registries[key][value] = object_to_register

    def set_user(self, key, user):
        self.__set_value_at_key(key, 'user', user)

    def set_env(self, key, env):
        self.__set_value_at_key(key, 'env', env)

    def set_group(self, key, name, group):
        self.__set_value_at_key(key, name, group)

    def set_propargs(self, key, propargs):
        self.__set_value_at_key(key, 'props', propargs)

    def does_key_exists(self, key):
        if key not in self.registries:
            raise KeyError(
                "key - {} does not exist in registry. "
                "Maybe you forgot to call create_new_execution_registry".format
                (key)
            )

    def get_propargs(self, key=COMMANDLINE_EXECUTION_KEY,
                     default_propargs=None):
        self.does_key_exists(key)
        if "props" not in self.registries[key]:
            return default_propargs
        return self.registries[key]["props"]

    def register_agent(self, key_to_register_agent_with, agent,
                       key=COMMANDLINE_EXECUTION_KEY):
        self.does_key_exists(key)
        if "agents" not in self.registries[key]:
            self.registries[key]["agents"] = {}
        self.registries[key]["agents"][key_to_register_agent_with] = agent

    def get_registered_agent(self, agent_name, key=COMMANDLINE_EXECUTION_KEY):
        self.does_key_exists(key)
        if agent_name not in self.registries[key]["agents"]:
            raise KeyError(
                "Agent with name - {} is not registered with key - {}".format(
                    agent_name, key))
        return self.registries[key]["agents"][agent_name]

    def get_registered_env(self, key=COMMANDLINE_EXECUTION_KEY):
        self.does_key_exists(key)
        if "env" not in self.registries[key]:
            raise KeyError(
                "No env registered for key - {}. Maybe you forgot to call set_env".format(
                    key))
        return self.registries[key]["env"]

    def get_registered_user(self, key=COMMANDLINE_EXECUTION_KEY):
        self.does_key_exists(key)
        if "user" not in self.registries[key]:
            raise KeyError(
                "No user registered for key - {}. Maybe you forgot to call set_user".format(
                    key))
        return self.registries[key]["user"]

    def get_registered_group(self, group_name, key=COMMANDLINE_EXECUTION_KEY):
        self.does_key_exists(key)
        if group_name not in self.registries[key]:
            raise KeyError(
                "Group - {} not registered for execution against execution_key - {}".format(
                    group_name, key))

        return self.registries[key].get(group_name)

    def get_execution_key_as_prop(self, key):
        return {
            VALUE: key,
            ATYPE: INT,
            HIVAL: None,
            LOWVAL: None
        }

    def clear_data_for_execution_key(self, key):
        if key != COMMANDLINE_EXECUTION_KEY:
            self.does_key_exists(key)
            del self.registries[key]


def is_model_ported_to_new_registry(model_id=None, model_name=None):
    if model_id is not None:
        return model_id not in []
    elif model_name is not None:
        return model_name not in []
    return False


def get_exec_key(kwargs):
    return check_and_get_execution_key_from_args(kwargs)


def check_and_get_execution_key_from_args(kwargs):
    execution_key = COMMANDLINE_EXECUTION_KEY
    if EXECUTION_KEY_NAME in kwargs:
        execution_key = kwargs[EXECUTION_KEY_NAME]
    return execution_key


execution_registry = ExecutionRegistry()

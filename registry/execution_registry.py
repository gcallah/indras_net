from registry import registry
from numpy import random
from propargs.constants import VALUE, ATYPE, INT, HIVAL, LOWVAL

BILLION = 10 ** 9

CLI_EXEC_KEY = 0

EXEC_KEY = "execution_key"


def init_exec_key(props=None):
    return int(props[EXEC_KEY].val) if props is not None else CLI_EXEC_KEY


class ExecutionRegistry(object):
    def __init__(self):
        print("Creating new registry")
        self.registries = {}
        self.registries[CLI_EXEC_KEY] = {}

    def get_unique_key(self):
        key = random.randint(1, BILLION)
        while key in self.registries.keys():
            key = random.randint(1, BILLION)
        return key

    def register(self, agent_registry: registry):
        key = self.get_unique_key()
        self.registries[key] = agent_registry

    def create_new_execution_registry(self):
        key = self.get_unique_key()
        print("Creating new execution_registry with key-{}".format(key))
        self.registries[key] = {}
        return key

    def __set_value_at_key(self, key=CLI_EXEC_KEY, value=None,
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
            print("Registry has - ", self.registries.keys())
            raise KeyError(
                "key - {} does not exist in registry. "
                "Maybe you forgot to call create_new_execution_registry".format
                (key)
            )

    def get_propargs(self, key=CLI_EXEC_KEY,
                     default_propargs=None):
        self.does_key_exists(key)
        if "props" not in self.registries[key]:
            return default_propargs
        return self.registries[key]["props"]

    def register_agent(self, key_to_register_agent_with, agent,
                       key=CLI_EXEC_KEY):
        self.does_key_exists(key)
        if "agents" not in self.registries[key]:
            self.registries[key]["agents"] = {}
        self.registries[key]["agents"][key_to_register_agent_with] = agent

    def get_registered_agent(self, agent_name, key=CLI_EXEC_KEY):
        self.does_key_exists(key)
        if agent_name not in self.registries[key]["agents"]:
            raise KeyError(
                "Agent with name - {} is not registered with key - {}".format(
                    agent_name, key))
        return self.registries[key]["agents"][agent_name]

    def get_registered_env(self, key=CLI_EXEC_KEY):
        self.does_key_exists(key)
        if "env" not in self.registries[key]:
            raise KeyError(
                "No env registered for key {}.".format(
                    key))
        return self.registries[key]["env"]

    def get_registered_user(self, key=CLI_EXEC_KEY):
        self.does_key_exists(key)
        if "user" not in self.registries[key]:
            raise KeyError(
                "No user registered for key {}.".format(
                    key))
        return self.registries[key]["user"]

    def get_registered_group(self, group_name, key=CLI_EXEC_KEY):
        self.does_key_exists(key)
        if group_name not in self.registries[key]:
            raise KeyError(
                "Group {} not registered for execution against key {}".format(
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
        if key != CLI_EXEC_KEY:
            self.does_key_exists(key)
            print("Clearing key - {} from registry".format(key))
            del self.registries[key]


def get_exec_key(kwargs):
    execution_key = CLI_EXEC_KEY
    if EXEC_KEY in kwargs:
        execution_key = kwargs[EXEC_KEY]
    return execution_key


print('Setting up execution registry for the server')
execution_registry = ExecutionRegistry()

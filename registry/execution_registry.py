from registry import registry
from numpy import random
from propargs.constants import *

BILLION = 10 ** 9

COMMANDLINE_EXECUTION_KEY = 0

EXECUTION_KEY_NAME = "execution_key"

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

    def __set_value_at_key(self, key, value, object_to_register):
        key = int(key)
        if key not in self.registries:
            raise KeyError(
                "key - {} does not exist in the Execution registry. "
                "Maybe you forgot to call create_new_execution_registry".format(
                    key))
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
                "key - {} does not exist in registry. Maybe you forgot to call create_new_execution_registry".format(
                    key
                )
            )

    def get_propargs(self, key):
        self.does_key_exists(key)
        if "props" not in self.registries[key]:
            raise KeyError(
                "Props have not been registered for key-{}. Maybe you forgot to call set_propargs".format(key))
        return self.registries[key]["props"]

    def register_agent(self, key, key_to_register_agent_with, agent):
        self.does_key_exists(key)
        if "agents" not in self.registries[key]:
            self.registries[key]["agents"] = {}
        self.registries[key]["agents"][key_to_register_agent_with] = agent

    def get_registered_agent(self, key, agent_name):
        self.does_key_exists(key)
        if agent_name not in self.registries[key]["agents"]:
            raise KeyError("Agent with name - {} is not registered with key")
        return self.registries[key]["agents"][agent_name]

    def get_registered_env(self, key):
        self.does_key_exists(key)
        if "env" not in self.registries[key]:
            raise KeyError("No env registered for key - {}. Maybe you forgot to call set_env".format(key))
        return self.registries[key]["env"]

    def get_registered_user(self, key):
        self.does_key_exists(key)
        if "user" not in self.registries[key]:
            raise KeyError("No user registered for key - {}. Maybe you forgot to call set_user".format(key))
        return self.registries[key]["user"]

    def get_registered_group(self, key, group_name):
        self.does_key_exists(key)
        if group_name not in self.registries[key]:
            raise KeyError("Group - {} not registered for execution against execution_key - {}".format(group_name, key))

        return self.registries[key].get(group_name)

    def get_execution_key_as_prop(self, key):
        return {
            VALUE: key,
            ATYPE: INT,
            HIVAL: None,
            LOWVAL: None
        }

    def clear_data_for_execution_key(self, key):
        self.does_key_exists(key)
        del self.registries[key]


execution_registry = ExecutionRegistry()

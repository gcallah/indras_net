"""
The intention behind creating this module is to regularize the
restoration of objects that cannot be directly serialized.
This class will appear as a dictionary, but with the right sort of default
behaviors that we need for our registry.
"""
import json
import warnings

from registry.execution_registry import execution_registry, \
    CLI_EXEC_KEY, EXEC_KEY, get_exec_key

REGISTRY = "Registry"

"""
We can also have some global singletons here. We'll start with `_the_user`;
"""
_the_user = None  # this is a singleton, so global should be ok
NOT_IMPL = "Choice not yet implemented."


def set_user(user):
    global _the_user
    _the_user = user


def user_tell(msg):
    if _the_user is None:
        print(msg)
    else:
        return _the_user.tell(msg)


def user_debug(msg):
    if _the_user is None:
        print(msg)
    else:
        return _the_user.debug(msg)


def user_log(msg):
    if _the_user is None:
        print(msg)
    else:
        return _the_user.log(msg)


def user_log_err(msg):
    return user_log("ERROR: " + msg)


def log_err_and_tell_user(msg):
    user_log_err(msg)
    user_tell(msg)


def user_log_warn(msg):
    return user_log("WARNING: " + msg)


def user_log_notif(msg):
    return user_log("NOTIFICATION: " + msg)


def run_notice(model_nm):
    return user_log_notif("Running model " + model_nm)


def not_impl(user):
    return _the_user.tell(NOT_IMPL)


_the_env = None  # this is a singleton, so global should be ok


def set_env(env):
    global _the_env
    _the_env = env


def get_env(execution_key=CLI_EXEC_KEY, **kwargs):
    if EXEC_KEY in kwargs:
        execution_key = get_exec_key(kwargs)
    return execution_registry.get_registered_env(execution_key)


def get_env_attr(key, execution_key=CLI_EXEC_KEY,
                 default_value=None):
    """
    A convenience function, since this will be
    used often.
    Returns None by default if env is not registered in any key
    """
    return execution_registry.get_registered_env(execution_key)\
        .get_attr(key, default=default_value)


def set_env_attr(key, val, execution_key=CLI_EXEC_KEY):
    """
    A convenience function, since this will be
    used often.
    """
    return execution_registry.get_registered_env(execution_key).set_attr(key,
                                                                         val)


"""
Our singleton dict for groups.
"""
_groups_dict = {}


def add_group(name, grp, execution_key=CLI_EXEC_KEY):
    execution_registry.set_group(execution_key, name, grp)


def get_group(name, execution_key=CLI_EXEC_KEY, **kwargs):
    if EXEC_KEY in kwargs:
        execution_key = get_exec_key(kwargs)
    return execution_registry.get_registered_group(group_name=name,
                                                   key=execution_key)


"""
Our singleton for properties.
"""
_the_props = None


def set_propargs(props):
    """
    Set the global props object.
    """
    global _the_props
    _the_props = props


def get_propargs():
    """
    Get the global props object: shouldn't generally need
    this; instead use next function.
    """
    return _the_props


def get_prop(prop_key, default_val=None,
             execution_key=CLI_EXEC_KEY):
    """
    Get a particular property.
    If key is missing (or no props) return default_val.
    """
    prop_args = execution_registry.get_propargs(key=execution_key,
                                                default_propargs=None)
    if prop_args is None:
        return default_val
    else:
        return prop_args.get(prop_key, default_val)
    # if _the_props is None:
    #     return default_val
    # else:
    #     return _the_props.get(key, default_val)


class Registry(object):
    """
    This is an abstraction layer over a dictionary of object names.
    As objects are restored from a serilazed stream, they should be
    registered here. If they are already registered, they will
    ignore the newly registered object, and leave the old value in place.
    """

    def __init__(self):
        self.agents = {}

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return json.dumps(self.to_json(), indent=4)

    def __getitem__(self, key):
        return self.agents[key]

    def __delitem__(self, key):
        del self.agents[key]

    def clear(self):
        self.agents.clear()

    def get(self, key, default=None):
        if key in self.agents:
            return self.__getitem__(key)
        else:
            return default

    def __setitem__(self, key, value):
        if key not in self.agents or self.agents[key] is None:
            self.agents[key] = value
            if value is None:
                warnings.warn("Trying to set the value of key {} to None.".
                              format(key), RuntimeWarning)
        else:
            pass
            # The problem with this exception is that tests
            # must clear the registry each test!
            # raise KeyError("The key \"{}\" already exists in the registry"
            #                .format(key))

    def __contains__(self, item):
        return item in self.agents

    def __iter__(self):
        return iter(self.agents)

    def to_json(self):
        """
        For right now, just list what keys are in the registry.
        """
        return {REGISTRY: str(self.agents.keys())}


registry = Registry()


def register(name_of_entity, entity, execution_key=CLI_EXEC_KEY):
    execution_registry.register_agent(name_of_entity, entity,
                                      key=execution_key)


def get_registration(name_of_entity, execution_key=CLI_EXEC_KEY):
    return execution_registry.get_registered_agent(name_of_entity,
                                                   key=execution_key)


def clear_registry():
    registry.clear()

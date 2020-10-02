_the_user = None


def set_user(user):
    global _the_user
    _the_user = user


def get_user():
    return _the_user


def user_tell(msg):
    if _the_user is not None:
        return _the_user.tell(msg)


def user_log(msg):
    if _the_user is not None:
        return _the_user.log(msg)


def user_log_notif(msg):
    return user_log("NOTIFICATION: " + msg)


def user_log_err(msg):
    return user_log("ERROR: " + msg)

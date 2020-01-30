
"""
This is the place to register functions passed as parameters,
which means that the API Server will need to re-locate them
whenever a new round of actions are requested.
"""

# We just need wolfsheep here at present!
creators_dict = {
    "create_sheep": create_sheep,
    "create_wolf": create_wolf,
}

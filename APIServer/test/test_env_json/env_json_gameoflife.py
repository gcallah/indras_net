def ret():
    return {
        "name": "Game of Life",
        "type": "env",
        "duration": 9223372036854775805,
        "pos": None,
        "attrs": {
            "size": 100,
            "change_grid_spacing": 1,
            "hide_xy_ticks": True,
            "hide_legend": True
        },
        "groups": [],
        "active": True,
        "type_sig": 0,
        "prim_group": None,
        "locator": None,
        "neighbors": None,
        "action_key": "gameoflife_action",
        "members": {
            "Black": {
                "name": "Black",
                "type": "composite",
                "duration": 9223372036854775805,
                "pos": None,
                "attrs": {
                    "color": "black",
                    "marker": "s"
                },
                "groups": [
                    "Game of Life"
                ],
                "active": True,
                "type_sig": 0,
                "prim_group": "Game of Life",
                "locator": None,
                "neighbors": None,
                "action_key": None,
                "members": {
                    "(16,16)": {
                        "name": "(16,16)",
                        "type": "agent",
                        "duration": 9223372036854775805,
                        "pos": [
                            16,
                            16
                        ],
                        "attrs": {},
                        "groups": [
                            "Black",
                            "Moore neighbors"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Black",
                        "locator": "Game of Life",
                        "neighbors": "Moore neighbors",
                        "action_key": "game_agent_action"
                    },
                    "(16,15)": {
                        "name": "(16,15)",
                        "type": "agent",
                        "duration": 9223372036854775805,
                        "pos": [
                            16,
                            15
                        ],
                        "attrs": {},
                        "groups": [
                            "Black",
                            "Moore neighbors"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Black",
                        "locator": "Game of Life",
                        "neighbors": "Moore neighbors",
                        "action_key": "game_agent_action"
                    },
                    "(15,14)": {
                        "name": "(15,14)",
                        "type": "agent",
                        "duration": 9223372036854775805,
                        "pos": [
                            15,
                            14
                        ],
                        "attrs": {},
                        "groups": [
                            "Black",
                            "Moore neighbors"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Black",
                        "locator": "Game of Life",
                        "neighbors": "Moore neighbors",
                        "action_key": "game_agent_action"
                    },
                    "(16,14)": {
                        "name": "(16,14)",
                        "type": "agent",
                        "duration": 9223372036854775806,
                        "pos": [
                            16,
                            14
                        ],
                        "attrs": {},
                        "groups": [
                            "Black",
                            "Moore neighbors"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Black",
                        "locator": "Game of Life",
                        "neighbors": "Moore neighbors",
                        "action_key": "game_agent_action"
                    },
                    "(14,15)": {
                        "name": "(14,15)",
                        "type": "agent",
                        "duration": 9223372036854775806,
                        "pos": [
                            14,
                            15
                        ],
                        "attrs": {},
                        "groups": [
                            "Black",
                            "Moore neighbors"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Black",
                        "locator": "Game of Life",
                        "neighbors": "Moore neighbors",
                        "action_key": "game_agent_action"
                    }
                }
            }
        },
        "width": 30,
        "height": 30,
        "locations": {
            "(16,16)": [
                16,
                16
            ],
            "(16,15)": [
                16,
                15
            ],
            "(15,14)": [
                15,
                14
            ],
            "(16,14)": [
                16,
                14
            ],
            "(14,15)": [
                14,
                15
            ]
        },
        "user": {
            "user_msgs": "",
            "name": "ziruizhou"
        },
        "census_func": None,
        "plot_title": "Game of Life",
        "props": {
            "grid_height": {
                "val": 30,
                "question": "What height would you like for the grid?",
                "atype": "INT",
                "lowval": 20,
                "hival": 200
            },
            "grid_width": {
                "val": 30,
                "question": "What width would you like for the grid?",
                "atype": "INT",
                "lowval": 20,
                "hival": 200
            },
            "simulation": {
                "val": 0,
                "question": None,
                "atype": None,
                "lowval": None,
                "hival": None
            },
            "use_line": {
                "val": True,
                "question": None,
                "atype": None,
                "lowval": None,
                "hival": None
            },
            "user_type": {
                "val": "terminal",
                "question": None,
                "atype": None,
                "lowval": None,
                "hival": None
            },
            "OS": {
                "val": "Darwin",
                "question": None,
                "atype": None,
                "lowval": None,
                "hival": None
            },
            "use_scatter": {
                "val": True,
                "question": None,
                "atype": None,
                "lowval": None,
                "hival": None
            }
        },
        "pop_hist": {
            "periods": 2,
            "pops": {
                "Black": [
                    0,
                    5,
                    5
                ]
            }
        },
        "womb": [],
        "switches": [],
        "data_func": None,
        "registry": {}
    }

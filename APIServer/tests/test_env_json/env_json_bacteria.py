def ret():
    return {
        "name": "Petrie dish",
        "type": "env",
        "duration": 9223372036854775805,
        "pos": None,
        "attrs": {},
        "groups": [],
        "active": True,
        "type_sig": 0,
        "prim_group": None,
        "locator": None,
        "neighbors": None,
        "action_key": None,
        "members": {
            "Toxins": {
                "name": "Toxins",
                "type": "composite",
                "duration": 9223372036854775805,
                "pos": None,
                "attrs": {
                    "color": "red"
                },
                "groups": [
                    "Petrie dish"
                ],
                "active": True,
                "type_sig": 0,
                "prim_group": "Petrie dish",
                "locator": None,
                "neighbors": None,
                "action_key": None,
                "members": {
                    "Toxins0": {
                        "name": "Toxins0",
                        "type": "agent",
                        "duration": 9223372036854775805,
                        "pos": [
                            14,
                            10
                        ],
                        "attrs": {
                            "max_move": 1
                        },
                        "groups": [
                            "Toxins"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Toxins",
                        "locator": "Petrie dish",
                        "neighbors": None,
                        "action_key": "toxin_action"
                    }
                }
            },
            "Nutrients": {
                "name": "Nutrients",
                "type": "composite",
                "duration": 9223372036854775805,
                "pos": None,
                "attrs": {
                    "color": "yellow"
                },
                "groups": [
                    "Petrie dish"
                ],
                "active": True,
                "type_sig": 0,
                "prim_group": "Petrie dish",
                "locator": None,
                "neighbors": None,
                "action_key": None,
                "members": {
                    "Nutrients0": {
                        "name": "Nutrients0",
                        "type": "agent",
                        "duration": 9223372036854775805,
                        "pos": [
                            8,
                            15
                        ],
                        "attrs": {
                            "max_move": 1
                        },
                        "groups": [
                            "Nutrients"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Nutrients",
                        "locator": "Petrie dish",
                        "neighbors": None,
                        "action_key": "nutrient_action"
                    }
                }
            },
            "Bacteria": {
                "name": "Bacteria",
                "type": "composite",
                "duration": 9223372036854775805,
                "pos": None,
                "attrs": {
                    "color": "green"
                },
                "groups": [
                    "Petrie dish"
                ],
                "active": True,
                "type_sig": 0,
                "prim_group": "Petrie dish",
                "locator": None,
                "neighbors": None,
                "action_key": None,
                "members": {
                    "Bacteria0": {
                        "name": "Bacteria0",
                        "type": "agent",
                        "duration": 9223372036854775805,
                        "pos": [
                            0,
                            11.583650153762417
                        ],
                        "attrs": {
                            "prev_toxicity": -0.008196721311475409,
                            "prev_nutricity": 0.024390243902439025,
                            "angle": 323,
                            "max_move": 3
                        },
                        "groups": [
                            "Bacteria"
                        ],
                        "active": True,
                        "type_sig": 0,
                        "prim_group": "Bacteria",
                        "locator": "Petrie dish",
                        "neighbors": None,
                        "action_key": "bacterium_action"
                    }
                }
            }
        },
        "width": 20,
        "height": 20,
        "locations": {
            "Toxins0": [
                14,
                10
            ],
            "Nutrients0": [
                8,
                15
            ],
            "Bacteria0": [
                0,
                11.583650153762417
            ]
        },
        "user": {
            "user_msgs": "",
            "name": "ziruizhou"
        },
        "census_func": None,
        "plot_title": "Petrie dish",
        "props": {
            "grid_height": {
                "val": 20,
                "question": "What is the grid height?",
                "atype": "INT",
                "lowval": 2,
                "hival": 100
            },
            "grid_width": {
                "val": 20,
                "question": "What is the grid width?",
                "atype": "INT",
                "lowval": 2,
                "hival": 100
            },
            "num_toxins": {
                "val": 1,
                "question": "How many toxins do you want?",
                "atype": "INT",
                "lowval": 1,
                "hival": 100
            },
            "threshold": {
                "val": -0.22,
                "question": "What toxin concentration threshold do you want?",
                "atype": "DBL",
                "lowval": -1,
                "hival": -0.01
            },
            "toxin_move": {
                "val": 1,
                "question": "What toxin maximum move do you want?",
                "atype": "INT",
                "lowval": 1,
                "hival": 5
            },
            "num_nutrients": {
                "val": 1,
                "question": "How many nutrients do you want?",
                "atype": "INT",
                "lowval": 1,
                "hival": 100
            },
            "nutrient_move": {
                "val": 1,
                "question": "What nutrient maximum move do you want?",
                "atype": "INT",
                "lowval": 1,
                "hival": 10
            },
            "num_bacteria": {
                "val": 1,
                "question": "How many bacteria do you want?",
                "atype": "INT",
                "lowval": 1,
                "hival": 100
            },
            "bacterium_move": {
                "val": 3,
                "question": "What bacterium maximum move do you want?",
                "atype": "INT",
                "lowval": 1,
                "hival": 15
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
            "use_line": {
                "val": True,
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
                "Toxins": [
                    1,
                    1,
                    1
                ],
                "Nutrients": [
                    1,
                    1,
                    1
                ],
                "Bacteria": [
                    1,
                    1,
                    1
                ]
            }
        },
        "womb": [],
        "switches": [],
        "data_func": None,
        "registry": {}
    }

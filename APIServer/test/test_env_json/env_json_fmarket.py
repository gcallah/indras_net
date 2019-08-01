def ret():
    return {
    "name": "env",
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
        "value_investors": {
            "name": "value_investors",
            "type": "composite",
            "duration": 9223372036854775805,
            "pos": None,
            "attrs": {
                "color": "blue"
            },
            "groups": [
                "env"
            ],
            "active": True,
            "type_sig": 0,
            "prim_group": "env",
            "locator": None,
            "neighbors": None,
            "action_key": None,
            "members": {
                "value_investors0": {
                    "name": "value_investors0",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        562,
                        9
                    ],
                    "attrs": {
                        "low_price": 9.199403731937808,
                        "high_price": 10.00081326736259,
                        "capital": 836.0,
                        "num_stock": 20
                    },
                    "groups": [
                        "value_investors"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "value_investors",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "value_investor_action"
                },
                "value_investors1": {
                    "name": "value_investors1",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        482,
                        36
                    ],
                    "attrs": {
                        "low_price": 9.54051013872484,
                        "high_price": 10.956325646873058,
                        "capital": 836.0,
                        "num_stock": 20
                    },
                    "groups": [
                        "value_investors"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "value_investors",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "value_investor_action"
                },
                "value_investors2": {
                    "name": "value_investors2",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        243,
                        997
                    ],
                    "attrs": {
                        "low_price": 9.565368020314205,
                        "high_price": 10.264013586736425,
                        "capital": 836.0,
                        "num_stock": 20
                    },
                    "groups": [
                        "value_investors"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "value_investors",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "value_investor_action"
                }
            }
        },
        "trend_followers": {
            "name": "trend_followers",
            "type": "composite",
            "duration": 9223372036854775805,
            "pos": None,
            "attrs": {
                "color": "red"
            },
            "groups": [
                "env"
            ],
            "active": True,
            "type_sig": 0,
            "prim_group": "env",
            "locator": None,
            "neighbors": None,
            "action_key": None,
            "members": {
                "trend_followers0": {
                    "name": "trend_followers0",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        321,
                        509
                    ],
                    "attrs": {
                        "change_period": 3.037143501449191,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers1": {
                    "name": "trend_followers1",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        226,
                        545
                    ],
                    "attrs": {
                        "change_period": 2.974684403718239,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers2": {
                    "name": "trend_followers2",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        531,
                        450
                    ],
                    "attrs": {
                        "change_period": 3.0768978004365812,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers3": {
                    "name": "trend_followers3",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        651,
                        274
                    ],
                    "attrs": {
                        "change_period": 3.0827432172214886,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers4": {
                    "name": "trend_followers4",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        106,
                        664
                    ],
                    "attrs": {
                        "change_period": 2.9590767132059814,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers5": {
                    "name": "trend_followers5",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        905,
                        759
                    ],
                    "attrs": {
                        "change_period": 3.0170748132126124,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers6": {
                    "name": "trend_followers6",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        65,
                        208
                    ],
                    "attrs": {
                        "change_period": 2.9643853420744017,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers7": {
                    "name": "trend_followers7",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        117,
                        84
                    ],
                    "attrs": {
                        "change_period": 2.954069339305682,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers8": {
                    "name": "trend_followers8",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        97,
                        65
                    ],
                    "attrs": {
                        "change_period": 3.0074701439470544,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                },
                "trend_followers9": {
                    "name": "trend_followers9",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        879,
                        292
                    ],
                    "attrs": {
                        "change_period": 3.0428990218779237,
                        "capital": 1000,
                        "num_stock": 0
                    },
                    "groups": [
                        "trend_followers"
                    ],
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "trend_followers",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "trend_follower_action"
                }
            }
        },
        "market_maker": {
            "name": "market_maker",
            "type": "agent",
            "duration": 9223372036854775805,
            "pos": [
                353,
                741
            ],
            "attrs": {
                "buy": 0,
                "sell": 0,
                "asset_price": 8.8,
                "prev_asset_price": 8.4,
                "price_hist": [
                    8,
                    8.4,
                    8.8
                ]
            },
            "groups": [
                "env"
            ],
            "active": True,
            "type_sig": 0,
            "prim_group": "env",
            "locator": "env",
            "neighbors": None,
            "action_key": "market_maker_action"
        }
    },
    "width": 1000,
    "height": 1000,
    "user": "ziruizhou",
    "census_func": None,
    "plot_title": "env",
    "props": {
        "value_investors": {
            "val": 3,
            "question": "How many value investors do you want?",
            "atype": "INT",
            "lowval": 1,
            "hival": 1000
        },
        "discount": {
            "val": 0.01,
            "question": "What % discount from 'True value' do the value investors want?",
            "atype": "DBL",
            "lowval": 0.01,
            "hival": 0.5
        },
        "deviation_investor": {
            "val": 0.05,
            "question": "What is the std deviation of that discount?",
            "atype": "DBL",
            "lowval": 0.001,
            "hival": 0.5
        },
        "trend_followers": {
            "val": 10,
            "question": "How many trend followers do you want?",
            "atype": "INT",
            "lowval": 1,
            "hival": 1000
        },
        "average_period": {
            "val": 3.0,
            "question": "What average number of periods do the trend followers want?",
            "atype": "DBL",
            "lowval": 1,
            "hival": 100
        },
        "deviation_follower": {
            "val": 0.05,
            "question": "What is the std deviation of that average number of periods?",
            "atype": "DBL",
            "lowval": 0.001,
            "hival": 0.5
        },
        "use_scatter": {
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
        "use_line": {
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
            "value_investors": [
                3,
                3,
                3
            ],
            "trend_followers": [
                10,
                10,
                10
            ],
            "market_maker": [
                1,
                0,
                0
            ]
        }
    },
    "womb": [],
    "switches": [],
    "data_func": None,
    "registry": {}
}

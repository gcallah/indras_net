#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""
import pytest
from unittest.mock import patch

from indra.prop_args_refactoring import PropArgs

NUM_AGENTS = "num_agents"
ANSWERS_FOR_INPUT_PROMPTS = [10]

@pytest.fixture
def prop_args():
    """
    A bare-bones prop_args object. To use - make `prop_args` a test argument.
    """
    with patch('builtins.input', side_effect=ANSWERS_FOR_INPUT_PROMPTS):
        return PropArgs.create_props("basic", props=None)

@pytest.mark.parametrize('lowval,test_val,hival,expected', [
        (None,  7, None, True),
        (None, -5,   10, True),
        (0,    99, None, True), 
        (0,     7,   10, True),
        (0,    77,   10, False),
        (0,    -5,   10, False)
        ])
def test_bounds(lowval, test_val, hival, expected, prop_args):
    prop_args[NUM_AGENTS].lowval = lowval
    prop_args[NUM_AGENTS].hival = hival

    assert prop_args._answer_within_bounds(prop_nm=NUM_AGENTS,
                                           typed_answer=test_val) \
           == expected


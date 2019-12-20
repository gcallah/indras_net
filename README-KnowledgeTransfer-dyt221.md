# Knowledge Transfer Document - dyt221

This semester, I updated the README several times with instructions that
hopefully will help future developers get started more quickly. I also improved
the `create_dev_env` target in the makefile under the same goal. I cleaned up
various Python files to improve overall compliance with PEP 8. I updated
[APIServer/api.sh](APIServer/api.sh) script to use the recommended method of
starting Flask. I modified the `/endpoints` endpoint on the API server to
compute the Flask app's registered endpoints dynamically. The previous version
used a hardcoded list.

I worked primarily on testing. I fixed some tests that were not running
inside the development Docker image. I changed the API server inside the
development Docker image to start in development mode instead of production
mode. I helped to retire `models/capital.py` in favor of the [models](models)
module by fixing a test that would crash without that file. I figured out why
[models/pytests.sh](models/pytests.sh) was running zero tests and fixed it.

I started to write replacement tests for `EnvTestCase.test_from_json` inside
[indra/tests/test_env.py](indra/tests/test_env.py). The test case is supposed
to test whether various classes are being deserialized properly. As it was
written, it actually was just putting hardcoded dictionaries through a
deserialization function, converting the return value's type to a string, and
comparing that string to a hardcoded one. I wrote one replacement test case,
called `test_env_json_plot_title`. It sets a property, serializes the object,
deserializes the object, and then checks that the value of that property
survived. More tests should be written for other properties. Eventually, the
entirety of [APIServer/test/test_env_json](APIServer/test/test_env_json) should
no longer be needed.

One more thing: look at `Agent.from_json` in [indra/agent.py](indra/agent.py).
I suspect that when `Env` in [indra/env.py](indra/env.py) is initialized with a
`serial_obj`, this function is getting called redundantly. It is called in
`Agent`'s constructor, which is called via `super()` in subclasses, but the
`from_json` methods of subclasses also seem to be calling `Agent.from_json` via
`super()`. I did not have the chance to investigate or verify this, but I
noticed this possible redundancy while reading the code.

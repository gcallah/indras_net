# This shell script runs the Indra API server.
# The user_type env var is needed to make user interactions within
# Indra behave properly.
export user_type="api"
python3 api_endpoints.py

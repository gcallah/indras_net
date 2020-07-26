# This shell script runs the Indra API server.
# The user_type env var is needed to make user interactions within
# Indra behave properly.
export user_type="api"
FLASK_APP=api_endpoints flask run --host=127.0.0.1 --port=8000

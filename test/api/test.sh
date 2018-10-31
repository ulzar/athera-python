$PYTHON_VERSION -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/../..

# Set these env vars, required for refreshing token:
# export ATHERA_API_CLIENT_ID=...
# export ATHERA_API_CLIENT_SECRET=...
nose2 -v --plugin nose2.plugins.junitxml --plugin refresh_token_plugin --junit-xml
deactivate

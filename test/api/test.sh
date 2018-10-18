$PYTHON_VERSION -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/../..
nose2 -v
deactivate

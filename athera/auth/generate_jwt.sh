export PYTHON_VERSION=python3
export PYTHONPATH=$(pwd)/../..

$PYTHON_VERSION -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$(pwd)/../..
$PYTHON_VERSION generate_jwt.py
deactivate

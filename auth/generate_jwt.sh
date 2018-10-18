export PYTHON_VERSION=python3.7

$PYTHON_VERSION -m venv venv
source venv/bin/activate
pip install -r requirements.txt
$PYTHON_VERSION generate_jwt.py
deactivate

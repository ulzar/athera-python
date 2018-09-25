python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd athera/test
nose2 -v
deactivate

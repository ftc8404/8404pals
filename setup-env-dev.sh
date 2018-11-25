python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
FLASK_APP=app/main.py flask run

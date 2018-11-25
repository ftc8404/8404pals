py -3 -m venv env
env\scripts\activate
pip install -r app\requirements.txt
Set-Item Env:FLASK_APP ".\app\main.py"

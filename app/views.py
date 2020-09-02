from flask import Flask, render_template, request, redirect, send_from_directory
import json
import os
from functools import wraps
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

import data
import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated

def requires_auth_api(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return "403 FORBIDDEN"
        return f(*args, **kwargs)

    return decorated

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.path.join(app.root_path, 'static'), 'favicon'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.route("/")
# def login():
#     return render_template("login2.html")

@app.route("/")
def hello():
    return render_template("home.html", data=data.getCompetitionOverviewData())


@app.route("/pre-game-scouting", methods=['GET', 'POST'])
@requires_auth
def pre_game_scouting():
    form = data.PreGameScoutingForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        error = data.validatePreGameScoutingForm(request.form)

        if(len(error)):
            form.error = error
            return render_template('pre-game-scouting.html', form=form)
        else:
            data.addPreGameScoutingEntry(request.form)

            return render_template('pre-game-scouting-success.html')

    return render_template('pre-game-scouting.html', form=form)


@app.route("/match-scouting", methods=['GET', 'POST'])
def match_scouting():
    form = data.MatchScoutingForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        error = data.validateMatchScoutingForm(request.form)

        if(len(error)):
            form.error = error
            return render_template('match-scouting.html', form=form)
        else:
            data.addMatchScoutingEntry(request.form)

            return render_template('match-scouting-success.html')

    return render_template('match-scouting.html', form=form)


@app.route("/team-info/<int:team_number>/", methods=['GET', 'POST'])
@requires_auth
def team(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    error = ""
    if request.method == 'POST':
        error = data.validateNotesForm(request.form)
        if error == "":
            data.addNoteEntry(
                team_number, request.form['tag'], request.form['message'])
    notes = data.getNoteEntries(team_number)

    return render_template('team-info.html', teamNumber=team_number, generalInfo=generalInfo, compInfo=compInfo, notes=notes, error=error)


@app.route("/team-info")
@requires_auth
def team_info():
    return render_template('team-info-search.html', data=data.getCompetitionOverviewData())


@app.route("/match-info", methods=['GET', 'POST'])
@requires_auth
def match_info():
    message = ''
    formValues = None
    largestMatch = 50
    if request.method == 'POST':
        formValues = request.form
        message, success, matchList, tempLargestMatch = data.validateMatchInfoForm(
            request.form)
        largestMatch = max(largestMatch, tempLargestMatch)
        if success:
            data.setMatchList(matchList)
            formValues = None

    matchList = data.getMatchList()
    matchNumbers = [int(matchNumberStr) for matchNumberStr in matchList]
    for matchNumber in matchNumbers:
        largestMatch = max(largestMatch, matchNumber)
    return render_template('match-info.html', formValues=formValues, message=message, data={"cityName": data.curCompetitionCityName, "id": data.curCompetitionId, "matchList": matchList, "tableRows": largestMatch})


@app.route("/competition-overview")
@requires_auth
def competition_overview():
    return render_template('competition-overview.html', data=data.getCompetitionOverviewData())


@app.route("/set-competition-id/<int:competition_id>/")
@requires_auth
def set_competition_id(competition_id):
    data.curCompetitionId = competition_id
    data.curCompetitionCityName = data.getCurCompetitionCityName()
    return "Current competition ID set to "+str(competition_id)


@app.route("/api/competition-overview/")
@requires_auth_api
def api_competition_overview():
    return json.dumps(data.getCompetitionOverviewData())

@app.route("/api/categories-list/")
@requires_auth_api
def api_categories_list():
    return json.dumps(data.getCategoriesList())


@app.route("/api/team-info/")
@app.route("/api/team-info/<int:team_number>/")
@requires_auth_api
def api_team_info(team_number=None):
    if team_number:
        generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
        return json.dumps({'generalInfo': generalInfo, 'performance': performanceInfo, 'compInfo': compInfo})
    else:
        rawData = data.getTeamsAtCompetition(data.curCompetitionId)
        dictData = {}
        for row in rawData:
            rowList = list(row)
            dictData[rowList[0]] = rowList[1]
        return json.dumps(dictData)


@app.route("/api/team-info/<int:team_number>/general/")
@requires_auth_api
def api_team_info_general(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(generalInfo)


@app.route("/api/team-info/<int:team_number>/performance/")
@requires_auth_api
def api_team_info_perf(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(performanceInfo)


@app.route("/api/team-info/<int:team_number>/matches/")
@requires_auth_api
def api_team_info_matches(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(compInfo['matches'])


@app.route("/api/match-results/")
@app.route("/api/match-results/<int:team_number>/")
@requires_auth_api
def api_match_results(team_number=None):
    matches = data.getMatchResults(teamNumber=team_number)
    return json.dumps(matches)


@app.route("/api/notes/<int:team_number>/")
@requires_auth_api
def api_notes(team_number):
    allNotes = data.getNoteEntries(team_number)
    allNotesFormatted = {}
    for i in range(len(allNotes)):
        allNotesFormatted[i] = allNotes[i]
    return json.dumps(allNotesFormatted)

@app.route('/login')
def login():
    session['logged_in'] = True
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

@app.route('/logout')
def logout():
    session.clear()
    session.pop('session')
    session['logged_in'] = False
    params = {'returnTo': url_for('hello', _external=True), 'client_id': AUTH0_CLIENT_ID}
    session.set_cookie('session', '', expires=0)
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')
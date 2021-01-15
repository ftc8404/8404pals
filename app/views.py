from flask.helpers import make_response
from app.data import SECRET_KEY
from flask import Flask, render_template, request, redirect, send_from_directory
import json
import os
from functools import wraps
import jwt

import data

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.path.join(app.root_path, 'static'), 'favicon'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.cookies:
            token = request.cookies['x-access-token']
        if not token:
            return redirect("/login?redirect=" + request.path)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return redirect("/login?redirect=" + request.path)
        return f(*args, **kwargs)

    return decorated

# @app.route("/")
# def login():
#     return render_template("login2.html")


@app.route("/")
def hello():
    return render_template("home.html", data=data.getCompetitionOverviewData())


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = data.LoginForm(request.form)
    print(form.errors)
    response = make_response(render_template("login.html", form=form))
    if request.method == 'POST':
        try:
            token = data.authenticateUser(
                request.form["email"], request.form["password"])
            print(token)
            redirect_path = request.args.get("redirect")
            if(redirect_path == None):
                redirect_path = "/"
            response = make_response(redirect(redirect_path))
            response.set_cookie("x-access-token", token,
                                86400, httponly=True)
        except ValueError:
            print("bad email/password")
            form.error = "Invalid email or password"
    return response


@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("x-access-token", "", 0)
    return response


@app.route("/pre-game-scouting", methods=['GET', 'POST'])
@token_required
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
@token_required
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
@token_required
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
@token_required
def team_info():
    return render_template('team-info-search.html', data=data.getCompetitionOverviewData())


@app.route("/match-info", methods=['GET', 'POST'])
@token_required
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
@token_required
def competition_overview():
    return render_template('competition-overview.html', data=data.getCompetitionOverviewData())


@app.route("/set-competition-id/<int:competition_id>/")
@token_required
def set_competition_id(competition_id):
    data.curCompetitionId = competition_id
    data.curCompetitionCityName = data.getCurCompetitionCityName()
    return "Current competition ID set to "+str(competition_id)


@app.route("/api/competition-overview/")
@token_required
def api_competition_overview():
    return json.dumps(data.getCompetitionOverviewData())


@app.route("/api/categories-list/")
@token_required
def api_categories_list():
    return json.dumps(data.getCategoriesList())


@app.route("/api/team-info/")
@app.route("/api/team-info/<int:team_number>/")
@token_required
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
@token_required
def api_team_info_general(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(generalInfo)


@app.route("/api/team-info/<int:team_number>/performance/")
@token_required
def api_team_info_perf(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(performanceInfo)


@app.route("/api/team-info/<int:team_number>/matches/")
@token_required
def api_team_info_matches(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(compInfo['matches'])


@app.route("/api/match-results/")
@app.route("/api/match-results/<int:team_number>/")
@token_required
def api_match_results(team_number=None):
    matches = data.getMatchResults(teamNumber=team_number)
    return json.dumps(matches)


@app.route("/api/notes/<int:team_number>/")
@token_required
def api_notes(team_number):
    allNotes = data.getNoteEntries(team_number)
    allNotesFormatted = {}
    for i in range(len(allNotes)):
        allNotesFormatted[i] = allNotes[i]
    return json.dumps(allNotesFormatted)

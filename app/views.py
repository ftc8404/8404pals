from flask import Flask, render_template, request, redirect
import json
import os

import data

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/pre-game-scouting", methods=['GET', 'POST'])
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


@app.route("/team-info/<int:team_number>/")
def team(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return render_template('team-info.html', teamNumber=team_number, generalInfo=generalInfo, compInfo=compInfo)


@app.route("/team-info")
def team_info():
    return redirect("/team-info/8404/")


@app.route("/match-info", methods=['GET', 'POST'])
def match_info():
    message = ''
    formValues = None
    if request.method == 'POST':
        formValues = request.form
        message, success, matchList = data.validateMatchInfoForm(request.form)
        if success:
            data.setMatchList(matchList)

    matchList = data.getMatchList()
    largestMatch = 150
    matchNumbers = [int(matchNumberStr) for matchNumberStr in matchList]
    for matchNumber in matchNumbers:
        largestMatch = max(largestMatch, matchNumber+1)
    return render_template('match-info.html', formValues=formValues, message=message, data={"cityName": data.curCompetitionCityName, "id": data.curCompetitionId, "matchList": data.getMatchList(), "tableRows": largestMatch})


@app.route("/competition-overview")
def competition_overview():
    return render_template('competition-overview.html', data=data.getCompetitionOverviewData())


@app.route("/set-competition-id/<int:competition_id>/")
def set_competition_id(competition_id):
    data.curCompetitionId = competition_id
    data.curCompetitionCityName = data.getCurCompetitionCityName()
    return "Current competition ID set to "+str(competition_id)


@app.route("/api/competition-overview/")
def api_competition_overview():
    return json.dumps(data.getCompetitionOverviewData())


@app.route("/api/team-info/")
@app.route("/api/team-info/<int:team_number>/")
def api_team_info(team_number=None):
    if team_number:
        generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
        return json.dumps({'generalInfo': generalInfo, 'performance': performanceInfo, 'compInfo': compInfo})
    else:
        rawData = data.getTeamsAtCompetition(data.curCompetitionId)
        dictData = {}
        for row in rawData:
            rowList=list(row)
            dictData[rowList[0]] = rowList[1]
        return json.dumps(dictData)


@app.route("/api/team-info/<int:team_number>/general/")
def api_team_info_general(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(generalInfo)


@app.route("/api/team-info/<int:team_number>/performance/")
def api_team_info_perf(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(performanceInfo)


@app.route("/api/team-info/<int:team_number>/matches/")
def api_team_info_matches(team_number):
    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return json.dumps(compInfo['matches'])

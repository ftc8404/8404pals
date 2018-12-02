from flask import Flask, render_template, request
import json

import data

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '8asdf98saf9d8f9sdf8sadf8as9dfds7f'


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
    return "This  site will eventually show information about team "+str(team_number)+"!"


@app.route("/team-info")
def team_info():
    pass


@app.route("/match-info", methods=['GET', 'POST'])
def match_info():
    message = ''
    if request.method == 'POST':
        message, success, matchList = data.validateMatchInfoForm(request.form)
        if success:
            pass
            # data.setMatchList()

    matchList = data.getMatchList()
    largestMatch = 50
    matchNumbers = [int(matchNumberStr) for matchNumberStr in matchList]
    for matchNumber in matchNumbers:
        largestMatch = max(largestMatch, matchNumber+1)
    return render_template('match-info.html', message=message, data={"cityName": data.curCompetitionCityName, "id": data.curCompetitionId, "matchList": data.getMatchList(), "tableRows": largestMatch})


@app.route("/competition-overview")
def competition_overview():
    return render_template('competition-overview.html', data=data.getCompetitionOverviewData())


@app.route("/set-competition-id/<int:competition_id>/")
def set_competition_id(competition_id):
    data.curCompetitionId = competition_id
    data.curCompetitionCityName = data.getCurCompetitionCityName()
    return "Current competition ID set to "+str(competition_id)


@app.route("/api/competition-overview-data")
def api_competition_overview_data():
    return json.dumps(data.getCompetitionOverviewData())

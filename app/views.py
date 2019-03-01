from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

import data
import oauth

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


@app.route("/")
def home():
    authenticated = oauth.check_if_auth()

    return render_template("home.html", authenticated=authenticated)


@app.route("/login-oauth")
def login_oauth():
    from_url = url_for('home')
    if(request.args.get('from')):
        from_url = request.args.get('from')
    session['auth_from_url'] = from_url
    return redirect(oauth.get_auth_url())


@app.route("/oauth2callback")
def oauth_callback():
    from_url = request.args.get('from')
    if(request.args.get('error') == None):
        auth_code = request.args.get('code')
        # oauth.getToken(auth_code)
        session['authenticated'] = True
        return redirect(session['auth_from_url'])
    else:
        return redirect(url_for('login_error'))


@app.route("/login-error")
def login_error():
    return "Not Authroized"


@app.route("/pre-game-scouting", methods=['GET', 'POST'])
def pre_game_scouting():
    if(not oauth.check_if_auth()):
        return redirect(oauth.get_login_url(url_for(request.endpoint)))

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
    if(not oauth.check_if_auth()):
        return redirect(oauth.get_login_url(url_for(request.endpoint)))

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
    if(not oauth.check_if_auth()):
        return redirect(oauth.get_login_url(url_for(request.endpoint)))

    generalInfo, performanceInfo, compInfo = data.getTeamInfo(team_number)
    return render_template('team-info.html', teamNumber=team_number, generalInfo=generalInfo, compInfo=compInfo)


@app.route("/team-info")
def team_info():
    if(not oauth.check_if_auth()):
        return redirect(oauth.get_login_url(url_for(request.endpoint)))

    return redirect("/team-info/8404/")


@app.route("/match-info", methods=['GET', 'POST'])
def match_info():
    if(not oauth.check_if_auth()):
        return redirect(oauth.get_login_url(url_for(request.endpoint)))

    message = ''
    formValues = None
    if request.method == 'POST':
        formValues = request.form
        message, success, matchList = data.validateMatchInfoForm(request.form)
        if success:
            data.setMatchList(matchList)

    matchList = data.getMatchList()
    largestMatch = 50
    matchNumbers = [int(matchNumberStr) for matchNumberStr in matchList]
    for matchNumber in matchNumbers:
        largestMatch = max(largestMatch, matchNumber+1)
    return render_template('match-info.html', formValues=formValues, message=message, data={"cityName": data.curCompetitionCityName, "id": data.curCompetitionId, "matchList": data.getMatchList(), "tableRows": largestMatch})


@app.route("/competition-overview")
def competition_overview():
    if(not oauth.check_if_auth()):
        return redirect(oauth.get_login_url(url_for(request.endpoint)))

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
            dictData[row[0]] = row[1]
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

from flask import Flask, render_template, request

import data

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '8asdf98saf9d8f9sdf8sadf8as9dfds7f'


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/pre-game-scouting", methods=['GET', 'POST'])
def pre_game_scouting():
    form = data.buildPreGameScoutingForm(request.form)
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


@app.route("/match-scouting")
def match_scouting():
    # return render_template("match-scouting.html")
    return "Not  yet implemented :("


@app.route("/team-info/<int:team_number>/")
def team(team_number):
    return "This  site will eventually show information about team "+str(team_number)+"!"


@app.route("/team-rankings")
def team_rankings():
    return "Not  yet implemented :("


@app.route("/competition-overview")
def competition_overview():
    return render_template('competition-overview.html', data=data.getCompetitionOverviewData())


@app.route("/set-competition-id/<int:competition_id>/")
def set_competition_id(competition_id):
    data.curCompetitionId = competition_id
    data.curCompetitionCityName = data.getCurCompetitionCityName()
    return "Current competition ID set to "+str(competition_id)

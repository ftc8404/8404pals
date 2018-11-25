from flask import Flask, render_template, flash, request
import wtforms

import pyodbc

server = 'quixilver8404data.database.windows.net'
database = 'quixilver8404data'
username = 'axchen7'
password = '7vE+xHxvC-a=~e6mMwcs*xg5S'
# driver = '{ODBC Driver 17 for SQL Server}'
driver = '{FreeTDS}'
sqlConn = pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                         ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password+';TDS_VERSION=8.0')
sqlCursor = sqlConn.cursor()


preGameScoutingTable = {
    "TeamNumber": "team_number", "Contact": "contact",
    "AutonLandCrater": "auton_crater_land", "AutonLandDepot": "auton_depot_land",
    "AutonSampleCrater": "auton_crater_sample", "AutonSampleDepot": "auton_depot_sample",
    "AutonDoubleSampleCrater": "auton_crater_double_sample", "AutonDoubleSampleDepot": "auton_depot_double_sample",
    "AutonMarkerCrater": "auton_crater_marker", "AutonMarkerDepot": "auton_depot_marker",
    "AutonParkCrater": "auton_crater_park", "AutonParkDepot": "auton_depot_park",
    "TeleopMineral": "teleop_minerals",
    "TeleopMineralCubes": "teleop_mineral_cubes", "TeleopMineralBalls": "teleop_mineral_balls",
    "TeleopCraterReach": "teleop_crater_reach", "TeleopCraterEnter": "teleop_crater_enter",
    "TeleopScoreCrater": "teleop_score_crater", "TeleopScoreDepot": "teleop_score_depot",
    "TeleopHang": "teleop_hang", "TeleopFullPark": "teleop_full_park"
}


def addPreGameScoutingEntry(formValues):
    tableFieldOrder = ""
    for tableField in preGameScoutingTable:
        tableFieldOrder += tableField+","
    tableFieldOrder = tableFieldOrder[:-1]

    formattedFormValues = ""
    for tableField, formField in preGameScoutingTable.items():
        if formField in formValues:
            formValue = formValues[formField]
            if formField == "contact":
                formattedFormValues += "'"+formValue+"'"
            elif formValue == "y":
                formattedFormValues += "1"
            else:
                formattedFormValues += str(formValue)
        else:
            formattedFormValues += "0"
        formattedFormValues += ","
    formattedFormValues = formattedFormValues[:-1]

    sqlCursor.execute("INSERT PreGameScoutingEntries ("+tableFieldOrder +
                      ",CompetitionId) VALUES ("+formattedFormValues+",1)")
    sqlConn.commit()


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '8asdf98saf9d8f9sdf8sadf8as9dfds7f'


def buildPreGameScoutingForm(*args):
    class PreGameScoutingForm(wtforms.Form):
        error = None

        team_number = wtforms.IntegerField("Team Number", validators=[
                                           wtforms.validators.required()])
        contact = wtforms.TextField("Contact / Web Page / Social Media", validators=[
            wtforms.validators.required()])

        auton_field_names = {
            "land": "Land", "sample": "Sample", "double_sample": "Double Sample",
            "marker": "Marker", "park": "Park"
        }

        teleop_minerals = wtforms.IntegerField("Estimated Minerals", validators=[
                                               wtforms.validators.required()])
        teleop_mineral_cubes = wtforms.BooleanField("Cubes")
        teleop_mineral_balls = wtforms.BooleanField("Balls")
        teleop_crater_reach = wtforms.BooleanField("Reach")
        teleop_crater_enter = wtforms.BooleanField("Enter")
        teleop_score_crater = wtforms.BooleanField("Crater")
        teleop_score_depot = wtforms.BooleanField("Depot")
        teleop_hang = wtforms.BooleanField("Hang")
        teleop_full_park = wtforms.BooleanField("Full Park")

    for field_name in PreGameScoutingForm.auton_field_names:
        setattr(PreGameScoutingForm, "auton_crater_" +
                field_name, wtforms.BooleanField("Crater"))
        setattr(PreGameScoutingForm, "auton_depot_" +
                field_name, wtforms.BooleanField("Depot"))
    return PreGameScoutingForm(*args)


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/pre-game-scouting", methods=['GET', 'POST'])
def pre_game_scouting():
    form = buildPreGameScoutingForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        error = ""
        teamNumber = 0
        teleopMinerals = 0.0
        try:
            teamNumber = int(request.form['team_number'])
        except ValueError:
            error = '"Team Number" must be a positive integer'
        try:
            teleopMinerals = float(request.form['teleop_minerals'])
        except ValueError:
            error = '"Estimated Minerals" must be a number from 0 - 150'
        if teamNumber <= 0:
            error = '"Team Number" must be a positive integer'
        if teleopMinerals < 0 or teleopMinerals > 150:
            error = '"Estimated Minerals" must be a number from 0 - 150'

        if(len(error)):
            form.error = error
            return render_template('pre-game-scouting.html', form=form)
        else:
            addPreGameScoutingEntry(request.form)

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


# if __name__ == "__main__":
#     app.run()

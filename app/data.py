import wtforms
import pyodbc

server = 'quixilver8404data.database.windows.net'
database = 'quixilver8404data'
username = 'axchen7'
password = '7vE+xHxvC-a=~e6mMwcs*xg5S'

driver = '{ODBC Driver 17 for SQL Server}'
# driver = '{FreeTDS}'

sqlConn = pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                         ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password+';TDS_VERSION=8.0')
sqlCursor = sqlConn.cursor()

curCompetitionId = 1
curCompetitionCityName = str(sqlCursor.execute(
    "SELECT * FROM Competitions WHERE CompetitionId="+str(curCompetitionId)).fetchall()[0][1])

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
    teamNumber = formValues["team_number"]
    exists = False
    if(len(sqlCursor.execute("SELECT * FROM PreGameScoutingEntries WHERE TeamNumber="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId)).fetchall()) > 0):
        exists = True

    tableFieldOrder = ""
    formattedFormValues = ""
    updateSet = ""
    for tableField, formField in preGameScoutingTable.items():
        tableFieldOrder += tableField+","
        nextformattedFormValues = ""
        if formField in formValues:
            formValue = formValues[formField]
            if formField == "contact":
                nextformattedFormValues = "'"+formValue+"'"
            elif formValue == "y":
                nextformattedFormValues = "1"
            else:
                nextformattedFormValues = str(formValue)
        else:
            nextformattedFormValues = "0"
        formattedFormValues += nextformattedFormValues+","
        updateSet += tableField+"="+nextformattedFormValues+","

    tableFieldOrder = tableFieldOrder[:-1]
    formattedFormValues = formattedFormValues[:-1]
    updateSet = updateSet[:-1]

    if(exists):
        sqlCursor.execute("UPDATE PreGameScoutingEntries SET "+updateSet +
                          " WHERE TeamNumber="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId))
    else:
        sqlCursor.execute("INSERT PreGameScoutingEntries ("+tableFieldOrder +
                          ",CompetitionId) VALUES ("+formattedFormValues+","+str(curCompetitionId)+")")
    sqlConn.commit()


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


def getCompetitionOverviewData():
    preGameScoutingData = []

    preGameScoutingFormData = [row[1:] for row in sqlCursor.execute(
        "SELECT * FROM PreGameScoutingEntries WHERE CompetitionId="+str(curCompetitionId)).fetchall()]
    for entry in preGameScoutingFormData:
        preGameScoutingData.append(dict(
            zip(preGameScoutingTable.keys(), entry)))
    competitionData = {
        "cityName": curCompetitionCityName, "id": curCompetitionId, "preGameScoutingData": preGameScoutingData}
    return competitionData

import wtforms
import pyodbc
import platform

server = 'quixilver8404data.database.windows.net'
database = 'quixilver8404data'
username = 'axchen7'
password = '7vE+xHxvC-a=~e6mMwcs*xg5S'

driver = ''
if platform.system() == 'Windows':
    driver = '{ODBC Driver 17 for SQL Server}'
else:
    driver = '{FreeTDS}'


def getSqlConn():
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                          ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password+';TDS_VERSION=8.0')


def getCurCompetitionCityName():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    curCompetitionCityName = str(sqlCursor.execute(
        "SELECT * FROM Competitions WHERE CompetitionId="+str(curCompetitionId)).fetchall()[0][1])
    sqlConn.close()
    return curCompetitionCityName


curCompetitionId = 21
curCompetitionCityName = getCurCompetitionCityName()


def getPreGameScoutingFields():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    fields = [row[0] for row in sqlCursor.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'PreGameScoutingEntries'").fetchall() if (row[0] != "EntryId" and row[0] != "CompetitionId")]
    sqlConn.close()
    return fields


preGameScoutingFields = getPreGameScoutingFields()


def getMatchScoutingFields():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    fields = [row[0] for row in sqlCursor.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'MatchScoutingEntries'").fetchall() if (row[0] != "EntryId" and row[0] != "CompetitionId")]
    sqlConn.close()
    return fields


matchScoutingFields = getMatchScoutingFields()


def getDataSummary(allTeamNumbers, preGameScoutingFormData, matchScoutingFormData):
    data = {}
    matchEntryCount = {}

    fields = ['Theoretical Auton Crater-Side Score', 'Theoretical Auton Depot-Side Score', 'Theoretical Auton Mean Score',
              'Theoretical Tele-Op Score', 'Theoretical Total Score', 'Match Auton Score', 'Match Tele-Op Score', 'Match Total Score']

    for teamNumber in allTeamNumbers:
        entryTeamNumber = str(teamNumber)
        data[entryTeamNumber] = ['N/A']*len(fields)
        matchEntryCount[entryTeamNumber] = 0

    for entry in preGameScoutingFormData:
        entryTeamNumber = str(entry[0])

        preAutonCraterScore = entry[2]*30+(50 if entry[6] else (
            25 if entry[4] else 0))+entry[8]*15+entry[10]*10
        preAutonDepotScore = entry[3]*30+(50 if entry[7] else (
            25 if entry[5] else 0))+entry[9]*15+entry[11]*10
        preAutonMeanScore = int(
            (preAutonCraterScore+preAutonDepotScore)/2)
        data[entryTeamNumber][0] = preAutonCraterScore
        data[entryTeamNumber][1] = preAutonDepotScore
        data[entryTeamNumber][2] = preAutonMeanScore

        preTeleopScore = entry[12]*(5 if entry[17] else (2 if entry[18] else 0))+(
            50 if entry[19] else (25 if entry[20] else 15))
        data[entryTeamNumber][3] = preTeleopScore
        data[entryTeamNumber][4] = preAutonMeanScore+preTeleopScore

    for entry in matchScoutingFormData:
        entryTeamNumber = str(entry[1])

        matchAutonScore = entry[2]*30+(50 if entry[4] else (
            25 if entry[3] else 0))+entry[5]*15+entry[6]*10
        matchTeleopScore = entry[7]*5+entry[8]*2 + \
            ({'none': 0, 'partial': 15, 'full': 25, 'hang': 50}[entry[9]])

        if matchEntryCount[entryTeamNumber] > 0:
            data[entryTeamNumber][5] += matchAutonScore
            data[entryTeamNumber][6] += matchTeleopScore
            data[entryTeamNumber][7] += matchAutonScore+matchTeleopScore
        else:
            data[entryTeamNumber][5] = matchAutonScore
            data[entryTeamNumber][6] = matchTeleopScore
            data[entryTeamNumber][7] = matchAutonScore+matchTeleopScore

        matchEntryCount[entryTeamNumber] += 1

    for teamNumber, amount in matchEntryCount.items():
        if amount > 0:
            data[str(teamNumber)][5] = round(
                data[str(teamNumber)][5]/amount, 1)
            data[str(teamNumber)][6] = round(
                data[str(teamNumber)][6]/amount, 1)
            data[str(teamNumber)][7] = round(
                data[str(teamNumber)][7]/amount, 1)

    return {'data': data, 'fields': fields}


def addPreGameScoutingEntry(formValues):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    teamNumber = formValues["team_number"]
    exists = False
    if(len(sqlCursor.execute("SELECT * FROM PreGameScoutingEntries WHERE team_number="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId)).fetchall()) > 0):
        exists = True

    tableFieldOrder = str(preGameScoutingFields).replace(
        "'", "").replace('"', "")[1:-1]
    formattedFormValues = ""
    updateSet = ""
    for field in preGameScoutingFields:
        nextformattedFormValues = ""
        if field in formValues:
            formValue = formValues[field]
            if field == "contact":
                nextformattedFormValues = "'"+formValue+"'"
            elif formValue == "y":
                nextformattedFormValues = "1"
            else:
                nextformattedFormValues = str(formValue)
        else:
            nextformattedFormValues = "0"
        formattedFormValues += nextformattedFormValues+","
        updateSet += field+"="+nextformattedFormValues+","

    formattedFormValues = formattedFormValues[:-1]
    updateSet = updateSet[:-1]

    if(exists):
        sqlCursor.execute("UPDATE PreGameScoutingEntries SET "+updateSet +
                          " WHERE team_number="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId))
    else:
        sqlCursor.execute("INSERT PreGameScoutingEntries ("+tableFieldOrder +
                          ",CompetitionId) VALUES ("+formattedFormValues+","+str(curCompetitionId)+")")
    sqlConn.commit()
    sqlConn.close()


def addMatchScoutingEntry(formValues):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    teamNumber = formValues["team_number"]
    matchNumber = formValues["match_number"]
    exists = False
    if(len(sqlCursor.execute("SELECT * FROM MatchScoutingEntries WHERE team_number="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId)+" AND match_number="+str(matchNumber)).fetchall()) > 0):
        exists = True

    tableFieldOrder = str(matchScoutingFields).replace(
        "'", "").replace('"', "")[1:-1]
    formattedFormValues = ""
    updateSet = ""
    for field in matchScoutingFields:
        nextformattedFormValues = ""
        if field in formValues:
            formValue = formValues[field]
            if field == "teleop_endgame":
                nextformattedFormValues = "'"+formValue+"'"
            elif formValue == "y":
                nextformattedFormValues = "1"
            else:
                nextformattedFormValues = str(formValue)
        else:
            nextformattedFormValues = "0"
        formattedFormValues += nextformattedFormValues+","
        updateSet += field+"="+nextformattedFormValues+","

    formattedFormValues = formattedFormValues[:-1]
    updateSet = updateSet[:-1]

    if(exists):
        sqlCursor.execute("UPDATE MatchScoutingEntries SET "+updateSet +
                          " WHERE team_number="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId)+" AND match_number="+str(matchNumber))
    else:
        sqlCursor.execute("INSERT MatchScoutingEntries ("+tableFieldOrder +
                          ",CompetitionId) VALUES ("+formattedFormValues+","+str(curCompetitionId)+")")
    sqlConn.commit()
    sqlConn.close()


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


class MatchScoutingForm(wtforms.Form):
    error = None

    match_number = wtforms.IntegerField("Match Number", validators=[
                                        wtforms.validators.required()])
    team_number = wtforms.IntegerField("Team Number", validators=[
                                       wtforms.validators.required()])

    auton_field_names = {
        "auton_land": "Land", "auton_sample": "Sample", "auton_double_sample": "Double Sample",
        "auton_marker": "Marker", "auton_park": "Park"
    }

    auton_field_names_row_1 = []
    auton_field_names_row_2 = []

    for item in auton_field_names:
        if len(auton_field_names_row_1) < 3:
            auton_field_names_row_1.append(item)
        else:
            auton_field_names_row_2.append(item)

    teleop_minerals_lander = wtforms.IntegerField("Minerals: Lander", validators=[
        wtforms.validators.required()])
    teleop_minerals_depot = wtforms.IntegerField("Minerals: Depot", validators=[
        wtforms.validators.required()])
    teleop_endgame = wtforms.SelectField("End", choices=[(
        "none", "None"), ("partial", "Partial Park"), ("full", "Full Park"), ("hang", "Hang")])


for field_name, natural_name in MatchScoutingForm.auton_field_names.items():
    setattr(MatchScoutingForm, field_name, wtforms.BooleanField(natural_name))


def validatePreGameScoutingForm(form):
    teamNumber = 0
    teleopMinerals = 0.0
    try:
        teamNumber = int(form['team_number'])
    except ValueError:
        return '"Team Number" must be a positive integer'

    if teamNumber <= 0:
        return '"Team Number" must be a positive integer'

    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    teamMatchAmount = len(sqlCursor.execute("SELECT * FROM TeamsAtCompetition(" +
                                            str(curCompetitionId)+") WHERE TeamNumber="+str(teamNumber)).fetchall())
    sqlConn.close()
    if teamMatchAmount == 0:
        return 'Team "'+str(teamNumber)+'" is not at this competition'

    try:
        teleopMinerals = float(form['teleop_minerals'])
    except ValueError:
        return '"Estimated Minerals" must be a number from 0 - 150'

    if teleopMinerals < 0 or teleopMinerals > 150:
        return '"Estimated Minerals" must be a number from 0 - 150'
    return ""


def validateMatchScoutingForm(form):
    teamNumber = 0
    try:
        teamNumber = int(form['team_number'])
    except ValueError:
        return '"Team Number" must be a positive integer'

    if teamNumber <= 0:
        return '"Team Number" must be a positive integer'

    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    teamMatchAmount = len(sqlCursor.execute("SELECT * FROM TeamsAtCompetition(" +
                                            str(curCompetitionId)+") WHERE TeamNumber="+str(teamNumber)).fetchall())
    sqlConn.close()
    if teamMatchAmount == 0:
        return 'Team "'+str(teamNumber)+'" is not at this competition'

    matchNumber = 0
    try:
        matchNumber = int(form['match_number'])
    except ValueError:
        return '"Match Number" must be a number from 1 - 500'

    if matchNumber < 1 or matchNumber > 150:
        return '"Match Number" must be a number from 1 - 500'

    landerMinerals = 0
    try:
        landerMinerals = int(form['teleop_minerals_lander'])
    except ValueError:
        return '"Minerals: Lander" must be a number from 0 - 150'

    if landerMinerals < 0 or landerMinerals > 150:
        return '"Minerals: Lander" must be a number from 0 - 150'

    depotMinerals = 0
    try:
        depotMinerals = int(form['teleop_minerals_depot'])
    except ValueError:
        return '"Minerals: Depot" must be a number from 0 - 150'

    if depotMinerals < 0 or depotMinerals > 150:
        return '"Minerals: Depot" must be a number from 0 - 150'

    return ""


def getCompetitionOverviewData():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    preGameScoutingFormData = [row[1:-1] for row in sqlCursor.execute(
        "SELECT * FROM PreGameScoutingEntries WHERE CompetitionId="+str(curCompetitionId)).fetchall()]
    allTeamNumbers = [str(row[0]) for row in sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition("+str(curCompetitionId)+")").fetchall()]
    matchScoutingFormData = [row[1:-1] for row in sqlCursor.execute(
        "SELECT * FROM MatchScoutingEntries WHERE CompetitionId="+str(curCompetitionId)).fetchall()]

    sqlConn.close()

    preGameScoutingData = {}

    for teamNumber in allTeamNumbers:
        preGameScoutingData[teamNumber] = [teamNumber]+["N/A"] * \
            (len(preGameScoutingFields)-1)

    summaryData = getDataSummary(allTeamNumbers, preGameScoutingFormData,
                                 matchScoutingFormData)

    for entry in preGameScoutingFormData:
        teamNumberStr = str(entry[0])
        preGameScoutingData[teamNumberStr] = list(entry)

    allData = {}
    for teamNumber in allTeamNumbers:
        teamNumberStr = str(teamNumber)
        allData[teamNumberStr] = preGameScoutingData[teamNumberStr] + \
            list(summaryData['data'][teamNumberStr])

    allTableKeys = preGameScoutingFields+summaryData['fields']

    competitionData = {
        "cityName": curCompetitionCityName, "id": curCompetitionId, "allData": allData, "tableKeys": allTableKeys}

    return competitionData

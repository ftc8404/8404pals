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
    teleop_score_lander = wtforms.BooleanField("Lander")
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

    if matchNumber < 1 or matchNumber > 500:
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


def validateMatchInfoForm(form):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    allTeamNumbers = [row[0] for row in sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition("+str(curCompetitionId)+")").fetchall()]
    sqlConn.close()

    teamList = {}
    curMatch = 1
    curMatchCount = 0
    for fieldName, value in form.items():
        matchNumber, teamIndex = tuple(
            [int(value2) for value2 in fieldName.split('_')])
        if value == '':
            continue
        try:
            teamNumber = int(value)
        except ValueError:
            return 'Error: Team Number must be a positive integer (match {match})'.format(match=str(matchNumber)), False, None
        if teamNumber <= 0:
            return 'Error: Team Number must be a positive integer (match {match})'.format(match=str(matchNumber)), False, None

        if teamNumber not in allTeamNumbers:
            return 'Error: Team {teamNumber} is not at this competition (match {match})'.format(teamNumber=str(teamNumber), match=str(matchNumber)), False, None

        if matchNumber != curMatch or teamIndex != curMatchCount:
            return "Error: missing data for match "+str(curMatch), False, None

        for teamIndex2 in range(teamIndex):
            if form[str(matchNumber)+'_'+str(teamIndex2)] == value:
                return "Error: duplicate team {team} (match {match})".format(team=value, match=str(matchNumber)), False, None

        if curMatchCount == 0:
            teamList[str(matchNumber)] = []
        teamList[str(matchNumber)].append(teamNumber)

        if curMatchCount == 3:
            curMatch += 1
            curMatchCount = 0
        else:
            curMatchCount += 1

    if curMatchCount != 0:
        return "Error: missing data for match "+str(curMatch),  False, None

    return "", True, teamList


def getTeamsAtCompetition(competitionId):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    data = sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition("+str(curCompetitionId)+")").fetchall()
    sqlConn.close()
    return data


def queryAllFormData():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    allTeamNumbers = [row[0] for row in sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition("+str(curCompetitionId)+")").fetchall()]
    preGameScoutingFormData = [row[1:-1] for row in sqlCursor.execute(
        "SELECT * FROM PreGameScoutingEntries WHERE CompetitionId="+str(curCompetitionId)).fetchall()]
    matchScoutingFormData = [row[1:-1] for row in sqlCursor.execute(
        "SELECT * FROM MatchScoutingEntries WHERE CompetitionId="+str(curCompetitionId)).fetchall()]

    sqlConn.close()
    return allTeamNumbers, preGameScoutingFormData, matchScoutingFormData


def getPreGameScoutingData(allTeamNumbers, preGameScoutingFormData):
    data = {}
    fields = []
    for field in preGameScoutingFields[1:]:
        fieldChars = list(field)
        uppercaseDist = ord('A')-ord('a')
        fieldChars[0] = chr(ord(fieldChars[0])+uppercaseDist)
        for i in range(len(fieldChars)):
            if(fieldChars[i] == '_' and i < len(fieldChars)-1):
                fieldChars[i] = ' '
                fieldChars[i+1] = chr(ord(fieldChars[i+1])+uppercaseDist)
        fields.append('Pre-Game '+''.join(fieldChars))

    for teamNumber in allTeamNumbers:
        data[teamNumber] = ["N/A"] * (len(fields))

    for entry in preGameScoutingFormData:
        teamNumber = entry[0]
        for i in range(len(entry)-1):
            data[teamNumber][i] = entry[i+1]

    return {'data': data, 'fields': fields}


def getMatchScoutingData(allTeamNumbers, matchScoutingFormData):
    data = {}
    matchEntryCount = {}
    fields = []
    for field in matchScoutingFields[2:]:
        fieldChars = list(field)
        uppercaseDist = ord('A')-ord('a')
        fieldChars[0] = chr(ord(fieldChars[0])+uppercaseDist)
        for i in range(len(fieldChars)):
            if(fieldChars[i] == '_' and i < len(fieldChars)-1):
                fieldChars[i] = ' '
                fieldChars[i+1] = chr(ord(fieldChars[i+1])+uppercaseDist)
        fields.append('Match '+''.join(fieldChars))

    for teamNumber in allTeamNumbers:
        data[teamNumber] = ['N/A']*len(fields)
        matchEntryCount[teamNumber] = 0

    for entry in matchScoutingFormData:
        teamNumber = entry[1]
        for i in range(len(fields)):
            n = entry[i+2]
            if i == 7:
                n = {'none': 0, 'partial': 15, 'full': 25, 'hang': 50}[n]
            if matchEntryCount[teamNumber] == 0:
                data[teamNumber][i] = n
            else:
                data[teamNumber][i] += n
        matchEntryCount[teamNumber] += 1

    for teamNumber, amount in matchEntryCount.items():
        if amount > 0:
            for i in range(len(fields)):
                data[teamNumber][i] /= amount

    return {'data': data, 'fields': fields}


def getDataSummary(allTeamNumbers, preGameScoutingFormData, matchScoutingFormData):
    data = {}
    matchEntryCount = {}

    fields = ['Theoretical Auton Crater-Side Score', 'Theoretical Auton Depot-Side Score', 'Theoretical Auton Mean Score',
              'Theoretical Tele-Op Score', 'Theoretical Total Score', 'Overall Match Auton Score', 'Overall Match Tele-Op Score', 'Overall Match Total Score']

    for teamNumber in allTeamNumbers:
        data[teamNumber] = ['N/A']*len(fields)
        matchEntryCount[teamNumber] = 0

    for entry in preGameScoutingFormData:
        teamNumber = entry[0]

        preAutonCraterScore = entry[2]*30+(50 if entry[6] else (
            25 if entry[4] else 0))+entry[8]*15+entry[10]*10
        preAutonDepotScore = entry[3]*30+(50 if entry[7] else (
            25 if entry[5] else 0))+entry[9]*15+entry[11]*10
        preAutonMeanScore = int(
            (preAutonCraterScore+preAutonDepotScore)/2)
        data[teamNumber][0] = preAutonCraterScore
        data[teamNumber][1] = preAutonDepotScore
        data[teamNumber][2] = preAutonMeanScore

        preTeleopScore = entry[12]*(5 if entry[17] else (2 if entry[18] else 0))+(
            50 if entry[19] else (25 if entry[20] else 15))
        data[teamNumber][3] = preTeleopScore
        data[teamNumber][4] = preAutonMeanScore+preTeleopScore

    for entry in matchScoutingFormData:
        teamNumber = entry[1]

        matchAutonScore = entry[2]*30+(50 if entry[4] else (
            25 if entry[3] else 0))+entry[5]*15+entry[6]*10
        matchTeleopScore = entry[7]*5+entry[8]*2 + \
            ({'none': 0, 'partial': 15, 'full': 25, 'hang': 50}[entry[9]])

        if matchEntryCount[teamNumber] > 0:
            data[teamNumber][5] += matchAutonScore
            data[teamNumber][6] += matchTeleopScore
            data[teamNumber][7] += matchAutonScore+matchTeleopScore
        else:
            data[teamNumber][5] = matchAutonScore
            data[teamNumber][6] = matchTeleopScore
            data[teamNumber][7] = matchAutonScore+matchTeleopScore

        matchEntryCount[teamNumber] += 1

    for teamNumber, amount in matchEntryCount.items():
        if amount > 0:
            data[teamNumber][5] = round(
                data[teamNumber][5]/amount, 1)
            data[teamNumber][6] = round(
                data[teamNumber][6]/amount, 1)
            data[teamNumber][7] = round(
                data[teamNumber][7]/amount, 1)

    return {'data': data, 'fields': fields}


def getCompetitionOverviewData():
    allTeamNumbers, preGameScoutingFormData, matchScoutingFormData = queryAllFormData()

    preGameScoutingData = getPreGameScoutingData(
        allTeamNumbers, preGameScoutingFormData)

    matchScoutingData = getMatchScoutingData(
        allTeamNumbers, matchScoutingFormData)

    summaryData = getDataSummary(allTeamNumbers, preGameScoutingFormData,
                                 matchScoutingFormData)

    allData = {}
    for teamNumber in allTeamNumbers:
        allData[teamNumber] = [teamNumber]+preGameScoutingData['data'][teamNumber] + \
            matchScoutingData['data'][teamNumber] + \
            (summaryData['data'][teamNumber])

    allTableKeys = ['Team Number']+preGameScoutingData['fields'] + \
        matchScoutingData['fields']+summaryData['fields']

    competitionData = {
        "cityName": curCompetitionCityName, "id": curCompetitionId, "allData": allData, "tableKeys": allTableKeys}

    return competitionData


def setMatchList(data, competitionId=curCompetitionId):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    sqlCursor.execute(
        "DELETE FROM MatchListEntries WHERE CompetitionId="+str(competitionId))
    for match, matchData in data.items():
        sqlCursor.execute(
            "INSERT MatchListEntries (CompetitionId, MatchNumber, Red1, Red2, Blue1, Blue2) VALUES ("+str(competitionId)+","+str(match)+","+str(matchData)[1:-1].replace('"', '').replace("'", '')+")")
    sqlConn.commit()
    sqlConn.close()


def getMatchList(competitionId=curCompetitionId):
    data = {}
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawData = sqlCursor.execute("SELECT * FROM MatchListEntries WHERE CompetitionId=" +
                                str(competitionId)).fetchall()
    sqlConn.close()
    for row in rawData:
        data[row[1]] = list(row[2:])
    return data


def getTeamInfo(teamNumber):
    generalInfo = {}
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawTeamData = sqlCursor.execute("SELECT * FROM Teams WHERE TeamNumber=" +
                                    str(teamNumber)).fetchall()
    generalInfo['teamNumber'] = teamNumber
    generalInfo['teamName'] = rawTeamData[0][1]
    quals = []
    for i in range(3):
        try:
            compId = int(rawTeamData[0][2+i])
        except TypeError:
            continue
        compDataRaw = sqlCursor.execute("SELECT * FROM Competitions WHERE CompetitionId=" +
                                        str(compId)).fetchall()[0]
        compName = compDataRaw[5]
        compCity = compDataRaw[1]
        compRegion = compDataRaw[2]
        compCountry = compDataRaw[3]
        compDate = compDataRaw[4]
        quals.append("{name} on {date} ({city}, {region}, {country})".format(
            name=compName, date=compDate, city=compCity, region=compRegion, country=compCountry))

    sqlConn.close()
    generalInfo['qualifiers'] = quals

    rawPerfData = getCompetitionOverviewData()['allData'][teamNumber]

    performanceInfo = {
        'preGame': {'auton': max(rawPerfData[29], rawPerfData[30]), 'teleOp': rawPerfData[32]},
        'match': {'auton': rawPerfData[34], 'teleOp': rawPerfData[35]}
    }

    compInfo = {}

    matchList = getMatchList()
    teamMatches = []
    for matchNumber, match in matchList.items():
        if teamNumber in match:
            curMatchEntry = {}
            opponents = {}
            curMatchEntry['number'] = matchNumber
            if teamNumber in match[0:2]:
                curMatchEntry['color'] = 'Red'
                opponents = match[2:4]
                alliance = match[1] if match[0] == teamNumber else match[0]
            else:
                curMatchEntry['color'] = 'Blue'
                opponents = match[0:2]
                alliance = match[3] if match[2] == teamNumber else match[2]
            curMatchEntry['opponent1'] = opponents[0]
            curMatchEntry['opponent2'] = opponents[1]
            curMatchEntry['alliance'] = alliance
            teamMatches.append(curMatchEntry)
    compInfo['matches'] = teamMatches

    return generalInfo, performanceInfo, compInfo

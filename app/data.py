import wtforms
import pyodbc
import platform
import os
from unidecode import unidecode

server = os.getenv('SQLCONNSTR_SERVER')
database = os.getenv('SQLCONNSTR_DATABASE')
username = os.getenv('SQLCONNSTR_USERNAME')
password = os.getenv('SQLCONNSTR_PASSWORD')

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


def addNoteEntry(teamNumber, tag, message):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    message = unidecode(message)
    message = message.replace("\r\n", "\n")
    message = message.replace("'", "''")

    tag = unidecode(tag)
    tag = tag.replace("'", "''")

    sqlCursor.execute("INSERT NoteEntries (team_number, tag, message, CompetitionId) VALUES (" +
                      str(teamNumber) + ", "+"'"+str(tag)+"'"+","+"'"+str(message)+"'"+","+str(curCompetitionId)+")")
    sqlConn.commit()
    sqlConn.close()


def getNoteEntries(teamNumber):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawNotes = sqlCursor.execute("SELECT tag, message FROM NoteEntries WHERE team_number="+str(
        teamNumber)+" AND CompetitionId="+str(curCompetitionId)).fetchall()
    sqlConn.close()
    formattedNotes = []
    for row in rawNotes:
        formattedRow = {}
        formattedRow['tag'] = row[0]
        formattedRow['message'] = row[1]
        formattedNotes.append(formattedRow)
    return formattedNotes


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

    notes = formValues["notes"]
    if len(notes) > 0:
        tag = "Pre-game observations"
        addNoteEntry(teamNumber, tag, notes)


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
            if formValue == "y":
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

    notes = formValues["notes"]
    if len(notes) > 0:
        tag = "Match observations"
        addNoteEntry(teamNumber, tag, notes)


class PreGameScoutingForm(wtforms.Form):
    error = None

    team_number = wtforms.IntegerField("Team Number", validators=[
        wtforms.validators.required()])
    contact = wtforms.TextField("Contact / Web Page / Social Media", validators=[
        wtforms.validators.required()])

    auton_stones = wtforms.IntegerField("Stones Delivered", validators=[
        wtforms.validators.required()])
    auton_skystone = wtforms.BooleanField("Detect Skystones")
    auton_foundation = wtforms.BooleanField("Reposition Foundation")
    auton_under_skybridge = wtforms.BooleanField("Move Under Skybridge")

    teleop_stones = wtforms.IntegerField("Stones Moved", validators=[
        wtforms.validators.required()])
    teleop_max_level = wtforms.IntegerField("Max Level", validators=[
        wtforms.validators.required()])
    teleop_cap = wtforms.BooleanField("Cap Team Marker")
    teleop_move_foundation = wtforms.BooleanField("Move Foundation")
    teleop_park = wtforms.BooleanField("Park")

    notes = wtforms.TextAreaField()


class MatchScoutingForm(wtforms.Form):
    error = None

    match_number = wtforms.IntegerField("Match Number", validators=[
                                        wtforms.validators.required()])
    team_number = wtforms.IntegerField("Team Number", validators=[
                                       wtforms.validators.required()])

    auton_stones = wtforms.IntegerField("Stones Delivered", validators=[
        wtforms.validators.required()])
    auton_skystone = wtforms.BooleanField("Detect Skystones")
    auton_foundation = wtforms.BooleanField("Reposition Foundation")
    auton_under_skybridge = wtforms.BooleanField("Move Under Skybridge")

    teleop_stones = wtforms.IntegerField("Stones Moved", validators=[
        wtforms.validators.required()])
    teleop_max_level = wtforms.IntegerField("Max Level", validators=[
        wtforms.validators.required()])
    teleop_cap = wtforms.BooleanField("Cap Team Marker")
    teleop_move_foundation = wtforms.BooleanField("Move Foundation")
    teleop_park = wtforms.BooleanField("Park")

    notes = wtforms.TextAreaField()


def checkASCII(text):
    return len(text) == len(text.encode())


def validateNotesForm(form):
    tag = form['tag']
    if len(tag) == 0:
        return '"Empty tag"'
    if len(tag) > 60:
        return '"Tag must not exceed 800 characters"'
    # if not checkASCII(tag):
    #     return '"Invalid characters in tag. Only ASCII characters are allowed."'

    message = form['message']
    if len(message) == 0:
        return '"Empty message"'
    if len(message) > 60:
        return '"Message must not exceed 800 characters"'
    # if not checkASCII(message):
    #     return '"Invalid characters in message. Only ASCII characters are allowed."'
    return ""


def validatePreGameScoutingForm(form):
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

    autonStones = 0
    try:
        autonStones = int(form['auton_stones'])
    except ValueError:
        return '"Stones Delivered" must be a number from 0 - 6'

    if autonStones < 0 or autonStones > 6:
        return '"Stones Delivered" must be a number from 0 - 6'

    teleopStones = 0
    try:
        teleopStones = int(form['teleop_stones'])
    except ValueError:
        return '"Stones Moved" must be a number from 0 - 30'

    if teleopStones < 0 or teleopStones > 30:
        return '"Stones Moved" must be a number from 0 - 30'
    notes = form['notes']
    if len(notes) > 800:
        return '"Notes must not exceed 800 characters"'
    if not checkASCII(notes):
        return '"Invalid characters in notes. Only ASCII characters are allowed."'

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

    matchList = getMatchList()
    if matchNumber in matchList and "del" not in matchList[matchNumber]:
        if teamNumber not in matchList[matchNumber]:
            return "Team " + str(teamNumber) + " is not in match "+str(matchNumber)

    autonStones = 0
    try:
        autonStones = int(form['auton_stones'])
    except ValueError:
        return '"Stones Delivered" must be a number from 0 - 6'

    if autonStones < 0 or autonStones > 6:
        return '"Stones Delivered" must be a number from 0 - 6'

    teleopStones = 0
    try:
        teleopStones = int(form['teleop_stones'])
    except ValueError:
        return '"Stones Moved" must be a number from 0 - 30'

    if teleopStones < 0 or teleopStones > 30:
        return '"Stones Moved" must be a number from 0 - 30'

    notes = form['notes']
    if len(notes) > 800:
        return '"Notes must not exceed 800 characters"'
    if not checkASCII(notes):
        return '"Invalid characters in notes. Only ASCII characters are allowed."'

    return ""


def validateMatchInfoForm(form):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    allTeamNumbers = [row[0] for row in sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition("+str(curCompetitionId)+")").fetchall()]
    sqlConn.close()

    teamList = {}
    matchesEntered = []
    largestMatch = 0
    for fieldName, value in form.items():
        matchNumber, teamIndex = tuple(
            [int(value2) for value2 in fieldName.split('_')])
        if value != '':
            largestMatch = max(largestMatch, matchNumber)

    for fieldName, value in form.items():
        matchNumber, teamIndex = tuple(
            [int(value2) for value2 in fieldName.split('_')])
        if value == '':
            if matchNumber in matchesEntered:
                return "Error: Incomplete data for match "+str(matchNumber), False, None, largestMatch
            continue
        if str(value).lower() == "del":
            teamNumber = "del"
        else:
            try:
                teamNumber = int(value)
            except ValueError:
                return 'Error: Team Number must be a positive integer (match {match})'.format(match=str(matchNumber)), False, None, largestMatch
            if teamNumber <= 0:
                return 'Error: Team Number must be a positive integer (match {match})'.format(match=str(matchNumber)), False, None, largestMatch

            if teamNumber not in allTeamNumbers:
                return 'Error: Team {teamNumber} is not at this competition (match {match})'.format(teamNumber=str(teamNumber), match=str(matchNumber)), False, None, largestMatch

            for teamIndex2 in range(teamIndex):
                if form[str(matchNumber)+'_'+str(teamIndex2)] == value:
                    return "Error: duplicate team {team} (match {match})".format(team=value, match=str(matchNumber)), False, None, largestMatch

        if matchNumber not in matchesEntered:
            if teamIndex > 0:
                return "Error: Incomplete data for match "+str(matchNumber), False, None, largestMatch
            teamList[str(matchNumber)] = []
            matchesEntered.append(matchNumber)
        teamList[str(matchNumber)].append(teamNumber)

    return "", True, teamList, largestMatch


def getAllTeamNames():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    data = sqlCursor.execute(
        "SELECT * FROM TEAMS").fetchall()
    data = [row[:2] for row in data]
    dictTeams = {}
    for row in data:
        dictTeams[row[0]] = row[1]
    sqlConn.close()
    return dictTeams


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
            if data[teamNumber][i] is True:
                data[teamNumber][i]=1
            elif data[teamNumber][i] is False:
                data[teamNumber][i]=0

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

    fields = ['Theoretical Auton Score', 'Theoretical Tele-Op Score', 'Theoretical Total Score',
              'Overall Match Auton Score', 'Overall Match Tele-Op Score', 'Overall Match Total Score']

    for teamNumber in allTeamNumbers:
        data[teamNumber] = ['N/A']*len(fields)
        matchEntryCount[teamNumber] = 0

    for entry in preGameScoutingFormData:
        teamNumber = entry[0]

        preAutonScore = entry[2]*(6 if entry[4] else 2) + \
            entry[3]*min(entry[2], 2)*8+entry[5]*10+entry[6]*5

        data[teamNumber][0] = preAutonScore

        preTeleopScore = entry[7]*1
        if entry[8] > 0:
            preTeleopScore += entry[7]*1
        preTeleopScore += entry[8]*2
        if entry[9]:
            preTeleopScore += entry[8]*1+5
        if entry[10]:
            preTeleopScore += 15
        if entry[11]:
            preTeleopScore += 5

        data[teamNumber][1] = preTeleopScore
        data[teamNumber][2] = preAutonScore+preTeleopScore

    for entry in matchScoutingFormData:
        teamNumber = entry[1]

        matchAutonScore = entry[2]*(6 if entry[4] else 2) + \
            entry[3]*min(entry[2], 2)*8+entry[5]*10+entry[6]*5
        matchTeleopScore = entry[7]*1
        if entry[8] > 0:
            matchTeleopScore += entry[7]*1
        matchTeleopScore += entry[8]*2
        if entry[9]:
            matchTeleopScore += entry[8]*1+5
        if entry[10]:
            matchTeleopScore += 15
        if entry[11]:
            matchTeleopScore += 5

        if matchEntryCount[teamNumber] > 0:
            data[teamNumber][3] += matchAutonScore
            data[teamNumber][4] += matchTeleopScore
            data[teamNumber][5] += matchAutonScore+matchTeleopScore
        else:
            data[teamNumber][3] = matchAutonScore
            data[teamNumber][4] = matchTeleopScore
            data[teamNumber][5] = matchAutonScore+matchTeleopScore

        matchEntryCount[teamNumber] += 1

    for teamNumber, amount in matchEntryCount.items():
        if amount > 0:
            data[teamNumber][3] = round(
                data[teamNumber][3]/amount, 1)
            data[teamNumber][4] = round(
                data[teamNumber][4]/amount, 1)
            data[teamNumber][5] = round(
                data[teamNumber][5]/amount, 1)

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
    for match, matchData in data.items():
        sqlCursor.execute(
            "DELETE FROM MatchListEntries WHERE MatchNumber="+str(match)+" AND CompetitionId="+str(curCompetitionId))
        if "del" not in [str(s).lower() for s in matchData]:
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


def getMatchResults(competitionId=curCompetitionId, teamNumber=None):
    matchList = getMatchList()

    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawData = sqlCursor.execute(
        "SELECT * FROM MatchScoutingEntries WHERE CompetitionId="+str(competitionId)).fetchall()
    sqlConn.close()
    matches = {}
    fields = getMatchScoutingFields()
    for row in rawData:
        curTeamNumber = row[2]
        curMatch = row[1]
        alliance = "unknown"
        if curMatch in matchList:
            if curTeamNumber in matchList[curMatch][:2]:
                alliance = "red"
            elif curTeamNumber in matchList[curMatch][2:]:
                alliance = "blue"

        if teamNumber:
            if curTeamNumber == teamNumber:
                teamDataDict = dict(zip(fields[2:], row[3:-1]))
                teamDataDict["alliance"] = alliance
                matches[curMatch] = teamDataDict
        else:
            if curMatch not in matches:
                matches[curMatch] = {}
            teamDataDict = dict(zip(fields[2:], row[3:-1]))
            teamDataDict["alliance"] = alliance
            matches[curMatch][curTeamNumber] = teamDataDict
    return matches


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
        'preGame': {'auton': rawPerfData[22], 'teleOp': rawPerfData[23]},
        'match': {'auton': rawPerfData[25], 'teleOp': rawPerfData[26]}
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

import wtforms
import wtforms.fields.html5
import pyodbc
import platform
import os
from unidecode import unidecode
import hashlib
import jwt

from wtforms.validators import ValidationError

SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

server = os.getenv('SQLCONNSTR_SERVER')
database = os.getenv('SQLCONNSTR_DATABASE')
username = os.getenv('SQLCONNSTR_USERNAME')
password = os.getenv('SQLCONNSTR_PASSWORD')


driver = ''
if platform.system() == 'Windows' or platform.system() == 'Darwin':
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
        "SELECT * FROM Competitions WHERE CompetitionId=?", str(curCompetitionId)).fetchall()[0][1])
    sqlConn.close()
    return curCompetitionCityName


curCompetitionId = 27
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

    sqlCursor.execute("INSERT NoteEntries (team_number, tag, message, CompetitionId) VALUES (?, ?, ?, ?)", str(
        teamNumber), str(tag), str(message), str(curCompetitionId))
    sqlConn.commit()
    sqlConn.close()


def getNoteEntries(teamNumber):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawNotes = sqlCursor.execute("SELECT tag, message FROM NoteEntries WHERE team_number=? AND CompetitionId=?", str(
        teamNumber), str(curCompetitionId)).fetchall()
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
    if(len(sqlCursor.execute("SELECT * FROM PreGameScoutingEntries WHERE team_number=? AND CompetitionId=?", str(teamNumber), str(curCompetitionId)).fetchall()) > 0):
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

    # TODO fix SQL injection
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
    if(len(sqlCursor.execute("SELECT * FROM MatchScoutingEntries WHERE team_number=? AND CompetitionId=? AND match_number=?", str(teamNumber), str(curCompetitionId), str(matchNumber)).fetchall()) > 0):
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

    # TODO fix SQL injection
    if(exists):
        sqlCursor.execute("UPDATE MatchScoutingEntries SET "+updateSet +
                          " WHERE team_number="+str(teamNumber)+" AND CompetitionId="+str(curCompetitionId)+" AND match_number="+str(matchNumber))
    else:
        sqlCursor.execute("INSERT MatchScoutingEntries ("+tableFieldOrder +
                          ",CompetitionId) VALUES ("+formattedFormValues+","+str(curCompetitionId)+")")

    # # #Categories lists

    catValue1 = 0
    catValue2 = 0
    catValue3 = 0
    catValue4 = 0
    catValue5 = 0
    catValue6 = 0
    catValue7 = 0
    catValue8 = 0
    catValue9 = 0
    catValue10 = 0
    catValue11 = 0
    catValue12 = 0

    field_name = 'feeder'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue1 = 1
    field_name = 'stacker'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue2 = 1
    field_name = 'speedy'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue3 = 1
    field_name = 'tall_lift'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue4 = 1
    field_name = 'under_bridge'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue5 = 1
    field_name = 'not_under_bridge'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue6 = 1
    field_name = 'knocked_tower'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue7 = 1
    field_name = 'DC'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue8 = 1
    field_name = 'dangerous_driving'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue9 = 1
    field_name = 'steps_over_bridge'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue10 = 1
    field_name = 'very_gp'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue11 = 1
    field_name = 'not_gp'
    if field_name in formValues and formValues[field_name] == 'y':
        catValue12 = 1

    if(len(sqlCursor.execute("SELECT * FROM Categories WHERE team_number=?", str(teamNumber)).fetchall()) == 0):
        sqlCursor.execute(
            "INSERT Categories (team_number) VALUES (?)", str(teamNumber))

    if (catValue1 == 1):
        sqlCursor.execute("UPDATE Categories SET feeder=? WHERE team_number=?", str(
            catValue1), str(teamNumber))
    if (catValue2 == 1):
        sqlCursor.execute("UPDATE Categories SET stacker=? WHERE team_number=?", str(
            catValue2), str(teamNumber))
    if (catValue3 == 1):
        sqlCursor.execute("UPDATE Categories SET speedy=? WHERE team_number=?", str(
            catValue3), str(teamNumber))
    if (catValue4 == 1):
        sqlCursor.execute("UPDATE Categories SET tall_lift=? WHERE team_number=?", str(
            catValue4), str(teamNumber))
    if (catValue5 == 1):
        sqlCursor.execute("UPDATE Categories SET under_bridge=? WHERE team_number=?", str(
            catValue5), str(teamNumber))
    if (catValue6 == 1):
        sqlCursor.execute("UPDATE Categories SET not_under_bridge=? WHERE team_number=?", str(
            catValue6), str(teamNumber))
    if (catValue7 == 1):
        sqlCursor.execute("UPDATE Categories SET knocked_tower=? WHERE team_number=?", str(
            catValue7), str(teamNumber))
    if (catValue8 == 1):
        sqlCursor.execute("UPDATE Categories SET dc=? WHERE team_number=?", str(
            catValue8), str(teamNumber))
    if (catValue9 == 1):
        sqlCursor.execute("UPDATE Categories SET dangerous_driving=? WHERE team_number=?", str(
            catValue9), str(teamNumber))
    if (catValue10 == 1):
        sqlCursor.execute("UPDATE Categories SET steps_over_bridge=? WHERE team_number=?", str(
            catValue10), str(teamNumber))
    if (catValue11 == 1):
        sqlCursor.execute("UPDATE Categories SET very_gp=? WHERE team_number=?", str(
            catValue11), str(teamNumber))
    if (catValue12 == 1):
        sqlCursor.execute("UPDATE Categories SET not_gp=? WHERE team_number=?", str(
            catValue12), str(teamNumber))

    sqlConn.commit()
    sqlConn.close()

    notes = formValues["notes"]
    if len(notes) > 0:
        tag = "Match observations"
        addNoteEntry(teamNumber, tag, notes)


class LoginForm(wtforms.Form):
    error = None

    email = wtforms.fields.html5.EmailField(
        "Email", validators=[wtforms.validators.required()])

    password = wtforms.PasswordField(
        "Password", validators=[wtforms.validators.required()])


class PreGameScoutingForm(wtforms.Form):
    error = None

    #General Labels
    team_number = wtforms.IntegerField("Team Number", validators=[
        wtforms.validators.required()])
    contact = wtforms.TextField("Contact / Web Page / Social Media", validators=[
        wtforms.validators.optional()])

    #Auton Labels
    auton_wobble = wtforms.IntegerField("Wobble Goal Delivered", validators=[
        wtforms.validators.optional()])
    auton_rings = wtforms.IntegerField("Rings Scored", validators=[
        wtforms.validators.optional()])
    auton_power = wtforms.BooleanField("Power Shots")
    auton_park = wtforms.BooleanField("Park")
    auton_high = wtforms.BooleanField("Rings in High Goal")
    auton_mid = wtforms.BooleanField("Rings in Mid Goal")
    auton_low = wtforms.BooleanField("Rings in Low Goal")
        
    #Teleop Labels
    teleop_rings = wtforms.IntegerField("Rings Scored", validators=[
        wtforms.validators.optional()])
    teleop_high = wtforms.BooleanField("Rings in High Goal")
    teleop_mid = wtforms.BooleanField("Rings in Mid Goal")
    teleop_low = wtforms.BooleanField("Rings in Low Goal")

    #End-Game Labels
    teleop_wobble = wtforms.IntegerField("Wobble Delivered", validators=[
        wtforms.validators.optional()])
    teleop_wobble_rings = wtforms.IntegerField("Wobble Rings", validators=[
        wtforms.validators.optional()])
    teleop_power = wtforms.BooleanField("Power Shots")
    teleop_wobble_start = wtforms.BooleanField("Wobble on Start")
    teleop_wobble_drop = wtforms.BooleanField("Wobble in Drop")
   
    notes = wtforms.TextAreaField()


class MatchScoutingForm(wtforms.Form):
    error = None

    match_number = wtforms.IntegerField("Match Number", validators=[
        wtforms.validators.required()])
    team_number = wtforms.IntegerField("Team Number", validators=[
        wtforms.validators.required()])

    auton_wobble = wtforms.IntegerField("Wobble Goals Delivered", validators=[
        wtforms.validators.optional()])
    auton_power = wtforms.IntegerField("Power Shots", validators=[
        wtforms.validators.optional()])
    auton_rings_high = wtforms.IntegerField("Rings in High Goal", validators=[
        wtforms.validators.optional()])
    auton_rings_mid = wtforms.IntegerField("Rings in Mid Goal", validators=[
        wtforms.validators.optional()])
    auton_rings_low = wtforms.IntegerField("Rings in Low Goal", validators=[
        wtforms.validators.optional()])
    auton_park = wtforms.BooleanField("Parking")

    teleop_rings_high = wtforms.IntegerField("Rings in High Goal", validators=[
        wtforms.validators.optional()])
    teleop_rings_mid = wtforms.IntegerField("Rings in Mid Goal", validators=[
        wtforms.validators.optional()])
    teleop_rings_low = wtforms.IntegerField("Rings in Low Goal", validators=[
        wtforms.validators.optional()])
    
    teleop_wobble_start = wtforms.IntegerField("Wobble on Start", validators=[
        wtforms.validators.optional()])
    teleop_wobble_drop = wtforms.IntegerField("Wobble in Drop", validators=[
        wtforms.validators.optional()])
    teleop_wobble_rings = wtforms.IntegerField("Rings on Wobble", validators=[
        wtforms.validators.optional()])
    teleop_power = wtforms.IntegerField("Power Shots", validators=[
        wtforms.validators.optional()])

    fast_intake = wtforms.BooleanField("Fast Intake")
    fast_shooter = wtforms.BooleanField("Fast Shooter")
    speedy = wtforms.BooleanField("Speedy")
    high_goal = wtforms.BooleanField("High Goal")
    power_shot = wtforms.BooleanField("Power Shots")
    accurate_shooter = wtforms.BooleanField("Accurate Shooter")
    wobble_goal = wtforms.BooleanField("Wobble Goal")
    DC = wtforms.BooleanField("DC :(")
    very_gp = wtforms.BooleanField("GP :)")
    not_gp = wtforms.BooleanField("Not GP :(")
    pog_human_player = wtforms.BooleanField("Pog Human Player")
    notes = wtforms.TextAreaField()


def checkASCII(text):
    return len(text) == len(text.encode())


def authenticateUser(email, password):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    potentialUser = sqlCursor.execute(
        "SELECT Name, PasswordHash, Salt, Id FROM Users WHERE Email=?", email).fetchall()
    sqlConn.close()

    if(len(potentialUser) == 0):
        raise ValueError("Email and password combination not valid")

    salt = potentialUser[0][2]
    curPasswordHash = hashlib.pbkdf2_hmac(
        "sha256", password.encode('utf-8'), salt, 100000, dklen=64)

    if(curPasswordHash == potentialUser[0][1]):
        id = potentialUser[0][3], "name"
        name = potentialUser[0][0]
        token = jwt.encode(
            {"id": id, "name": name}, SECRET_KEY, algorithm="HS256")
        return token
    else:
        raise ValueError("Email and password combination not valid")


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
    teamMatchAmount = len(sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition(?) WHERE TeamNumber=?", str(curCompetitionId), str(teamNumber)).fetchall())
    sqlConn.close()
    if teamMatchAmount == 0:
        return 'Team "'+str(teamNumber)+'" is not at this competition'

    # check if number of wobble goals delivered during auton is an integer between 0 - 2
    autonWobble = 0
    try:
        autonWobble = int(form['auton_wobble'])
    except ValueError:
        return '"Wobble Goals Delivered in Auton" must be a number from 0 - 2'
    if autonWobble < 0 or autonWobble > 2:
        return '"Wobble Goals Delivered in Auton" must be a number from 0 - 2'

    # check if number of rings scored during auton is an integer between 0 - 7
    autonRings = 0
    try:
        autonRings = int(form['auton_rings'])
    except ValueError:
        return '"Rings Scored in Auton" must be a number from 0 - 7'
    if autonRings < 0 or autonRings > 7:
        return '"Rings Scored in Auton" must be a number from 0 - 7'

    
    # check if number of rings scored in teleop is an integer between 0 - 40
    teleopRings = 0
    try:
        teleopRings = int(form['teleop_rings'])
    except ValueError:
        return '"Rings Scored in Teleop" must be a number from 0 - 40'

    if teleopRings < 0 or teleopRings > 40:
        return '"Rings Scored in Teleop" must be a number from 0 - 40'

    # check if number of wobble goals delivered is an integer between 0 - 2
    teleopWobble = 0
    try:
        teleopWobble = int(form['teleop_wobble'])
    except ValueError:
        return '"Wobble Goals delivered in End Game" must be a number from 0 - 2'

    if teleopWobble < 0 or teleopWobble > 2:
        return '"Wobble Goals delivered in End Game" must be a number from 0 - 2'

    # check if number of rings on wobble goals is an integer between 0 - 10
    teleopWobbleRings = 0
    try:
        teleopWobbleRings = int(form['teleop_wobble_rings'])
    except ValueError:
        return '"Wobble Goal Rings in End Game" must be a number from 0 - 10'

    if teleopWobbleRings < 0 or teleopWobbleRings > 10:
        return '"Wobble Goal Rings in End Game" must be a number from 0 - 10'

    notes = form['notes']
    if len(notes) > 800:
        return '"Notes must not exceed 800 characters"'
    if not checkASCII(notes):
        return '"Invalid characters in notes. Only ASCII characters are allowed."'

    return ""


def validateMatchScoutingForm(form):
    # validate all the data inputted to ensure bad data won't go into the database

    # check if team number is a positive integer
    teamNumber = 0
    try:
        teamNumber = int(form['team_number'])
    except ValueError:
        return '"Team Number" must be a positive integer'

    if teamNumber <= 0:
        return '"Team Number" must be a positive integer'

    # check if the team number is a team at the competition
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    teamMatchAmount = len(sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition(?) WHERE TeamNumber=?", str(curCompetitionId), str(teamNumber)).fetchall())
    sqlConn.close()
    if teamMatchAmount == 0:
        return 'Team "'+str(teamNumber)+'" is not at this competition'

    # check if match number is a positive integer 1 - 500
    matchNumber = 0
    try:
        matchNumber = int(form['match_number'])
    except ValueError:
        return '"Match Number" must be a number from 1 - 500'

    if matchNumber < 1 or matchNumber > 500:
        return '"Match Number" must be a number from 1 - 500'

    # check if the team number in in the match
    matchList = getMatchList()
    if matchNumber in matchList and "del" not in matchList[matchNumber]:
        if teamNumber not in matchList[matchNumber]:
            return "Team " + str(teamNumber) + " is not in match "+str(matchNumber)

    # check if number of stones delivered during auton is an integer between 1 - 6
    autonStones = 0
    try:
        autonStones = int(form['auton_stones'])
    except ValueError:
        return '"Stones Delivered" must be a number from 0 - 6'
    if autonStones < 0 or autonStones > 6:
        return '"Stones Delivered" must be a number from 0 - 6'

    # check if number of skystones delivered during auton is an integer between 1 - 2
    autonSkystones = 0
    try:
        autonSkystones = int(form['auton_skystones'])
    except ValueError:
        return '"Skystones Delivered" must be a number from 0 - 2'
    if autonSkystones < 0 or autonSkystones > 2:
        return '"Skystones Delivered" must be a number from 0 - 2'
    # check if number of skystones delivered in auton is less than or equal to number of total stones delivered
    if autonStones < autonSkystones:
        return '"Skystones Delivered" cannot be greater than "Stones Delivered"'

    # check if number of stones on the foundation is an integer 0-6
    autonStonesOnFoundation = 0
    try:
        autonStonesOnFoundation = int(form['auton_stones_on_foundation'])
    except ValueError:
        return '"Stones On Foundation" must be a number from 0 - 6'
    if autonStonesOnFoundation < 0 or autonStonesOnFoundation > 6:
        return '"Stones On Foundation" must be a number from 0 - 6'
    # check if number of stones on foundation is less than or equal to the number of stones delivered
    if autonStonesOnFoundation > autonStones:
        return '"Stones on Foundation" cannot be greater than "Stones Delivered"'

    # check if total stones moved in teleop is an integer between 0 - 30
    teleopStonesTotal = 0
    try:
        teleopStonesTotal = int(form['teleop_stones_total'])
    except ValueError:
        return '"Stones Moved" must be a number from 0 - 30'
    if teleopStonesTotal < 0 or teleopStonesTotal > 30:
        return '"Stones Moved" must be a number from 0 - 30'

    # check if the number of stones in stack 1 is an integer between 0 - 30
    teleopStones1 = 0
    try:
        teleopStones1 = int(form['teleop_stones_1'])
    except ValueError:
        return '"Stones in Stack" must be a number 0 - 30'
    if teleopStones1 < 0 or teleopStones1 > 30:
        return '"Stones in Stack" must be a number 0 - 30'

    # check if the number of stones in stack 2 is an integer between 0 - 30
    teleopStones2 = 0
    try:
        teleopStones2 = int(form['teleop_stones_2'])
    except ValueError:
        return '"Stones in Stack" must be a number 0 - 30'
    if teleopStones2 < 0 or teleopStones2 > 30:
        return '"Stones in Stack" must be a number 0 - 30'

    # check if the number of stones in stack 3 is an integer between 0 - 30
    teleopStones3 = 0
    try:
        teleopStones3 = int(form['teleop_stones_3'])
    except ValueError:
        return '"Stones in Stack" must be a number 0 - 30'
    if teleopStones3 < 0 or teleopStones3 > 30:
        return '"Stones in Stack" must be a number 0 - 30'

    # check if the number of stones in stack 4 is an integer between 0 - 30
    teleopStones4 = 0
    try:
        teleopStones4 = int(form['teleop_stones_4'])
    except ValueError:
        return '"Stones in Stack" must be a number 0 - 30'
    if teleopStones4 < 0 or teleopStones4 > 30:
        return '"Stones in Stack" must be a number 0 - 30'

    # check if there is less than or equal to one capstone placed
    numberOfCaps = 0
    for i in range(1, 5):
        field_name = 'teleop_cap_'+str(i)
        if field_name in form and form[field_name] == 'y':
            numberOfCaps += 1
    if numberOfCaps > 1:
        return 'Team can only place a Capstone once'

    notes = form['notes']
    if len(notes) > 800:
        return '"Notes must not exceed 800 characters"'
    if not checkASCII(notes):
        return '"Invalid characters in notes. Only ASCII characters are allowed."'

    return ""


def getCategoriesList():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    data = sqlCursor.execute(
        "SELECT * FROM Categories").fetchall()
    sqlConn.close()

    feeder_list = []
    stacker_list = []
    speedy_list = []
    tall_lift_list = []
    under_bridge_list = []
    not_under_bridge_list = []
    knocked_tower_list = []
    DC_list = []
    dangerous_driving_list = []
    steps_over_bridge_list = []
    very_gp_list = []
    not_gp_list = []

    for team in data:
        teamNumber = team[0]
        # Category Variables List
        if team[1]:
            feeder_list.append(teamNumber)
        if team[2]:
            stacker_list.append(teamNumber)
        if team[3]:
            speedy_list.append(teamNumber)
        if team[4]:
            tall_lift_list.append(teamNumber)
        if team[5]:
            under_bridge_list.append(teamNumber)
        if team[6]:
            not_under_bridge_list.append(teamNumber)
        if team[7]:
            knocked_tower_list.append(teamNumber)
        if team[8]:
            DC_list.append(teamNumber)
        if team[9]:
            dangerous_driving_list.append(teamNumber)
        if team[10]:
            steps_over_bridge_list.append(teamNumber)
        if team[11]:
            very_gp_list.append(teamNumber)
        if team[12]:
            not_gp_list.append(teamNumber)

    return feeder_list, stacker_list, speedy_list, tall_lift_list, under_bridge_list, not_under_bridge_list, knocked_tower_list, DC_list, dangerous_driving_list, steps_over_bridge_list, very_gp_list, not_gp_list


def validateMatchInfoForm(form):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    allTeamNumbers = [row[0] for row in sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition(?)", str(curCompetitionId)).fetchall()]
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
        "SELECT * FROM TeamsAtCompetition(?)", str(curCompetitionId)).fetchall()
    sqlConn.close()
    return data


def queryAllFormData():
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    allTeamNumbers = [row[0] for row in sqlCursor.execute(
        "SELECT * FROM TeamsAtCompetition(?)", str(curCompetitionId)).fetchall()]
    preGameScoutingFormData = [list(row[1:-1]) for row in sqlCursor.execute(
        "SELECT * FROM PreGameScoutingEntries WHERE CompetitionId=?", str(curCompetitionId)).fetchall()]
    matchScoutingFormData = [list(row[1:-1]) for row in sqlCursor.execute(
        "SELECT * FROM MatchScoutingEntries WHERE CompetitionId=?", str(curCompetitionId)).fetchall()]

    for i in range(len(preGameScoutingFormData)-1):
        for j in range(len(preGameScoutingFormData[i])-1):
            if preGameScoutingFormData[i][j] is True:
                preGameScoutingFormData[i][j] = 1
            elif preGameScoutingFormData[i][j] is False:
                preGameScoutingFormData[i][j] = 0

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


def getDataSummary(allTeamNumbers, preGameScoutingFormData, matchScoutingFormData):  # TODO
    data = {}
    matchEntryCount = {}

    fields = ['Theoretical Auton Score', 'Theoretical Tele-Op Score', 'Theoretical Total Score',
              'Overall Match Auton Score', 'Overall Match Tele-Op Score', 'Overall Match Total Score']

    for teamNumber in allTeamNumbers:
        data[teamNumber] = ['N/A']*len(fields)
        matchEntryCount[teamNumber] = 0
    for entry in preGameScoutingFormData:
        teamNumber = entry[0]

        # Auton score for Pre Game
        preAutonScore = 0 #create preAutonScore variable
        preAutonScore = entry[2]*15 # wobble goal delivery
        if entry[3]: # powershots
            preAutonScore += 45 
        if entry[4]: # rings in high goal
            preAutonScore += entry[7]*12
        elif entry[5]: # rings in mid goal
            preAutonScore += entry[7]*6
        elif entry[6]: # rings in low goal
            preAutonScore += entry[7]*3
        if entry[8]: # parking points
            preAutonScore += 5
        # Store Pre Game Auton Score in data array
        data[teamNumber][0] = preAutonScore


        #Teleop score for Pre Game
        preTeleopScore = 0
        if entry[9]: # rings in high goal
            preTeleopScore += entry[12]*6
        elif entry[10]: # rings in mid goal
            preTeleopScore += entry[12]*4
        elif entry[11]: # rings in low goal
            preTeleopScore += entry[12]*2
        if entry[13]: # wobble goals on start line
            preTeleopScore += entry[15]*5
        elif entry[14]: # wobble goals in drop zone
            preTeleopScore += entry[15]*20
        preTeleopScore += entry[16]*5 # rings on wobble goal
        if entry[17]: # power shots
            preTeleopScore += 45

        # Store Pre Game Teleop Score in data array
        data[teamNumber][1] = preTeleopScore
        # Store Pre Game Total Score in data array
        data[teamNumber][2] = preAutonScore+preTeleopScore

    for entry in matchScoutingFormData:
        teamNumber = entry[1]

        matchAutonScore = entry[2]*2 + \
            entry[3]*8 + entry[4]*4 + entry[5]*10 + entry[6]*5
        matchTeleopScore = entry[7]*2
        highestStack = 0
        StackList = [entry[8], entry[9], entry[10], entry[11]]
        for item in StackList:
            if item > highestStack:
                highestStack = item
        matchTeleopScore += highestStack*2
        CapList = [entry[12], entry[13], entry[14], entry[15]]
        capIndex = -1
        for item in CapList:
            if item:
                capIndex = CapList.index(item)
        if(capIndex != -1):
            matchTeleopScore += StackList[capIndex]*1+5
        if entry[16]:
            matchTeleopScore += 15
        if entry[17]:
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

    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()

    goldDivisionRaw = [sqlCursor.execute(
        "SELECT gold_division FROM Divisions").fetchall()]
    goldDivision = goldDivisionRaw[0]
    siliconDivisionRaw = [sqlCursor.execute(
        "SELECT silicon_division FROM Divisions").fetchall()]
    siliconDivision = siliconDivisionRaw[0]
    goldTeams = []
    siliconTeams = []

    index = 0
    for team in goldDivision:
        for item in team:
            if item == True:
                goldTeams.append(allTeamNumbers[index])
        index += 1

    index = 0
    for team in siliconDivision:
        for item in team:
            if item == True:
                siliconTeams.append(allTeamNumbers[index])
        index += 1

    for teamNumber in allTeamNumbers:
        allData[teamNumber] = [teamNumber]+preGameScoutingData['data'][teamNumber] + \
            matchScoutingData['data'][teamNumber] + \
            (summaryData['data'][teamNumber])

    allTableKeys = ['Team Number']+preGameScoutingData['fields'] + \
        matchScoutingData['fields']+summaryData['fields']

    competitionData = {
        "cityName": curCompetitionCityName, "id": curCompetitionId, "allData": allData, "tableKeys": allTableKeys, "goldDiv": goldTeams, "siliconDiv": siliconTeams}

    return competitionData


def setMatchList(data, competitionId=curCompetitionId):
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    for match, matchData in data.items():
        sqlCursor.execute(
            "DELETE FROM MatchListEntries WHERE MatchNumber=? AND CompetitionId=?", str(match), str(curCompetitionId))
        if "del" not in [str(s).lower() for s in matchData]:
            # TODO fix SQL injection
            sqlCursor.execute(
                "INSERT MatchListEntries (CompetitionId, MatchNumber, Red1, Red2, Blue1, Blue2) VALUES ("+str(competitionId)+","+str(match)+","+str(matchData)[1:-1].replace('"', '').replace("'", '')+")")
    sqlConn.commit()
    sqlConn.close()


def getMatchList(competitionId=curCompetitionId):
    data = {}
    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawData = sqlCursor.execute(
        "SELECT * FROM MatchListEntries WHERE CompetitionId=?", str(competitionId)).fetchall()
    sqlConn.close()
    for row in rawData:
        data[row[1]] = list(row[2:])
    return data


def getMatchResults(competitionId=curCompetitionId, teamNumber=None):
    matchList = getMatchList()

    sqlConn = getSqlConn()
    sqlCursor = sqlConn.cursor()
    rawData = sqlCursor.execute(
        "SELECT * FROM MatchScoutingEntries WHERE CompetitionId=?", str(competitionId)).fetchall()
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
    rawTeamData = sqlCursor.execute(
        "SELECT * FROM Teams WHERE TeamNumber=?", str(teamNumber)).fetchall()
    generalInfo['teamNumber'] = teamNumber
    generalInfo['teamName'] = rawTeamData[0][1]
    quals = []
    for i in range(3):
        try:
            compId = int(rawTeamData[0][2+i])
        except TypeError:
            continue
        compDataRaw = sqlCursor.execute(
            "SELECT * FROM Competitions WHERE CompetitionId=?", str(compId)).fetchall()[0]
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
        'preGame': {'auton': rawPerfData[40], 'teleOp': rawPerfData[41]},
        'match': {'auton': rawPerfData[43], 'teleOp': rawPerfData[44]}
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

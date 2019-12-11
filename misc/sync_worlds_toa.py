from selenium import webdriver
import pyodbc
import os

server = os.getenv('SQLCONNSTR_SERVER')
database = os.getenv('SQLCONNSTR_DATABASE')
username = os.getenv('SQLCONNSTR_USERNAME')
password = os.getenv('SQLCONNSTR_PASSWORD')
driver = '{ODBC Driver 17 for SQL Server}'

sqlConn = pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                         ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password+';TDS_VERSION=8.0')
sqlCursor = sqlConn.cursor()

driver = webdriver.Edge()

division = 1

if division == 0:
    driver.get("https://theorangealliance.org/events/1819-CMP-HOU1")
else:
    driver.get("https://theorangealliance.org/events/1819-CMP-HOU2")


teamEntries = driver.find_elements_by_tag_name("toa-team-item")
for teamEntry in teamEntries:
    teamNumber = teamEntry.find_elements_by_tag_name("div")[1].text
    teamName = teamEntry.find_elements_by_tag_name("span")[0].text
    if "Team #" in teamName:
        teamName = "["+teamNumber+"]"
    print(teamNumber+", "+teamName)
    # exists = False
    # if len(sqlCursor.execute("SELECT * FROM Teams WHERE TeamNumber="+str(teamNumber)).fetchall()) > 0:
    #     exists = True
    # if not exists:
    #     sqlCursor.execute(
    #         "INSERT Teams (TeamNumber, TeamName) VALUES ("+teamNumber+", "+"'"+teamName+"'"+")")

    exists = False
    if len(sqlCursor.execute("SELECT * FROM HoustonWorldChampionshipTeams WHERE TeamNumber="+str(teamNumber)).fetchall()) > 0:
        exists = True
    if not exists:
        sqlCursor.execute(
            "INSERT HoustonWorldChampionshipTeams (TeamNumber, Division) VALUES ("+teamNumber+", "+str(division)+")")
sqlConn.commit()

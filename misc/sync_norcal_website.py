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
driver.get("https://www.norcalftc.org/norcal-ftc-team-list/")

compIds = {"FRES": 2, "DUB": 7, "GGL": 8, "FREM": 9, "PIE": 10, "ALA": 11,
           "CSCO": 12, "WAL": 13, "MV": 14, "SC": 15, "INT": 16, "ROS": 17, "DALY": 18, "NAPA": 19, "BUR": 20, "SAR": 21, "RED": 22}

table = driver.find_element_by_tag_name("tbody")
for tRow in table.find_elements_by_tag_name("tr")[1:]:
    entries = tRow.find_elements_by_tag_name("td")
    if(entries[4].text == "No"):
        continue
    teamNumber = int(entries[0].text)
    teamName = entries[1].text
    city = entries[2].text
    comps = entries[6].text.split(", ")
    comp1 = 'NULL'
    comp2 = 'NULL'
    comp3 = 'NULL'
    if(len(comps) == 1 and comps[0] == "none"):
        pass
    else:
        if(len(comps) > 0):
            comp1 = compIds[comps[0]]
        if(len(comps) > 1):
            comp2 = compIds[comps[1]]
        if(len(comps) > 2):
            comp3 = compIds[comps[2]]

    command = "INSERT INTO Teams (TeamNumber, TeamName, CompetitionId1, CompetitionId2, CompetitionId3) VALUES (" + \
        str([teamNumber, teamName.replace("'s", "''s"), comp1, comp2, comp3])[
            1:-1].replace('"', "'").replace("'NULL'", "NULL")+")"
    print(command)
    sqlCursor.execute(command)

sqlConn.commit()

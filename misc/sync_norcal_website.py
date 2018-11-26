from selenium import webdriver
import pyodbc

server = 'quixilver8404data.database.windows.net'
database = 'quixilver8404data'
username = 'axchen7'
password = '7vE+xHxvC-a=~e6mMwcs*xg5S'
driver = '{ODBC Driver 17 for SQL Server}'

sqlConn = pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                         ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password+';TDS_VERSION=8.0')
sqlCursor = sqlConn.cursor()

driver = webdriver.Edge()
driver.get("https://www.norcalftc.org/norcal-ftc-team-list/")

table = driver.find_element_by_tag_name("tbody")
for tRow in table.find_elements_by_tag_name("tr")[1:]:
    entries = tRow.find_elements_by_tag_name("td")
    if(entries[4].text == "No"):
        continue
    teamNumber = int(entries[0].text)
    teamName = entries[1].text
    city = entries[2].text
    competitions = entries[6].text.split(", ")
    command = "INSERT INTO Teams (TeamNumber, TeamName) VALUES (" + \
        str([teamNumber, teamName.replace("'s", "''s")])[
            1:-1].replace('"', "'")+")"
    print(command)
    sqlCursor.execute(command)

sqlConn.commit()

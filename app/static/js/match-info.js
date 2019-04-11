var HttpreqTeam = new XMLHttpRequest(); // a new request
HttpreqTeam.open("GET", "/api/match-results/", false);
HttpreqTeam.send(null);
var matchResults = JSON.parse(HttpreqTeam.responseText);

var table = document.getElementById("matches-table")
var tableRows = table.rows
for (matchNumber in matchResults) {
    if (matchNumber <= tableRows.length - 1) {
        let curMatchEntries = matchResults[matchNumber]
        cells = tableRows[matchNumber].cells
        for (teamNumber in curMatchEntries) {
            for (let i = 1; i < 5; i++) {
                cell = cells[i]
                if (cell.children.length > 0 && cell.children[0].value == teamNumber) {
                    let teamMatchData = curMatchEntries[teamNumber]

                    let score = 0
                    if (teamMatchData["auton_land"]) score += 30;
                    if (teamMatchData["auton_sample"]) score += 25;
                    if (teamMatchData["auton_double_sample"]) score += 25;
                    if (teamMatchData["auton_marker"]) score += 15;
                    if (teamMatchData["auton_park"]) score += 10;
                    score += (teamMatchData["teleop_minerals_lander"] * 5);
                    score += (teamMatchData["teleop_minerals_depot"] * 2);
                    if (teamMatchData["teleop_endgame"] == "partial") score += 15;
                    else if (teamMatchData["teleop_endgame"] == "full") score += 25;
                    else if (teamMatchData["teleop_endgame"] == "hang") score += 50;

                    cell.innerHTML += "<p style=\"margin:0 0 0 0;\">" + score + " points</p>";
                    cell.children[1].addEventListener("click", clickScore);
                    break;
                }
            }
        }
    }
}

function clickScore(event) {
    event.srcElement.removeEventListener("click", clickScore);
    let teamNumber = event.srcElement.parentElement.children[0].value
    let matchNumber = event.srcElement.parentElement.parentElement.children[0].innerHTML;
    let data = matchResults[matchNumber][teamNumber]
    let text = ""
    text += "Auton land: " + (data["auton_land"] ? "yes" : "no") + "<br>";
    text += "Auton sample: " + (data["auton_sample"] ? "yes" : "no") + "<br>";
    text += "Auton double sample: " + (data["auton_double_sample"] ? "yes" : "no") + "<br>";
    text += "Auton marker: " + (data["auton_marker"] ? "yes" : "no") + "<br>";
    text += "Auton park: " + (data["auton_park"] ? "yes" : "no") + "<br>";
    text += "Tele-op minerals lander: " + data["teleop_minerals_lander"] + "<br>";
    text += "Tele-op minerals depot: " + data["teleop_minerals_depot"] + "<br>";
    text += "Tele-op endgame: " + data["teleop_endgame"];

    event.srcElement.parentElement.innerHTML += "<p style=\"margin:0 0 0 0;\">" + text + "</p>";
}
var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/team-info/", false);
Httpreq.send(null);
var teams = JSON.parse(Httpreq.responseText);

function search() {
    let text = document.getElementById("search").value;
    matches = match(text);
    teamNumbers = Object.keys(matches);
    if (text.length > 0 && teamNumbers.length > 0) {
        window.location.href = "/team-info/" + teamNumbers[0] + "/";
    }
}

function searchChange() {
    let text = document.getElementById("search").value;
    matches = match(text);
    populateResults(matches);
}

function match(text) {
    if (text.length == 0) {
        return {};
    }
    matches1 = {};
    matches2 = {};
    let count = 0;
    for (let teamNumber in teams) {
        teamName = teams[teamNumber];
        if (teamNumber.startsWith(text)) {
            matches1[teamNumber] = teamName;
            count++;
        }
        else if (teamName.toLowerCase().startsWith(text.toLowerCase())) {
            matches2[teamNumber] = teamName;
            count++;
        }
        if (count >= 20) {
            break;
        }
    }
    for (let k in matches2) {
        matches1[k] = matches2[k];
    }
    return matches1;
}

var resultsElement = document.getElementById("results");

function populateResults(matches) {
    resultsElement.innerHTML = "";
    for (teamNumber in matches) {
        let teamName = matches[teamNumber];
        let entryText = teamNumber + " " + teamName;
        let linkNode = document.createElement("a");
        linkNode.setAttribute("href", "/team-info/" + teamNumber + "/");
        let textNode = document.createTextNode(entryText);
        linkNode.appendChild(textNode);
        resultsElement.appendChild(linkNode);
        resultsElement.innerHTML += "<br>";
    }
}

searchChange();
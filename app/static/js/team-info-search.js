var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/team-info/", false);
Httpreq.send(null);
var teamsUnprocessed = JSON.parse(Httpreq.responseText);

var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/competition-overview/", false);
Httpreq.send(null);
var compData = JSON.parse(Httpreq.responseText);
var allData = compData.allData;

var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/categories-list/", false);
Httpreq.send(null);
var lists = JSON.parse(Httpreq.responseText);

// Category Variables List
var feeder_list = lists[0];
var stacker_list = lists[1];
var speedy_list = lists[2];
var tall_lift_list = lists[3];
var under_bridge_list = lists[4];
var not_under_bridge_list = lists[5];
var knocked_tower_list = lists[6];
var DC_list = lists[7];
var dangerous_driving_list = lists[8];
var steps_over_bridge_list = lists[9];
var very_gp_list = lists[10];
var not_gp_list = lists[11];


var match_feeder = false;
var match_stacker = false;
var match_speedy = false;
var match_tall_lift = false;
var match_under_bridge = false;
var match_not_under_bridge = false;
var match_knocked_tower = false;
var match_DC = false;
var match_dangerous_driving = false;
var match_steps_over_bridge = false;
var match_very_gp = false;
var match_not_gp = false;

function changeFilter(checkboxElem) {
    if (checkboxElem.id == "Match Feeder Bot") {
        match_feeder = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Stacking Bot") {
        match_stacker = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Speedy") {
        match_speedy = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Tall Lift") {
        match_tall_lift = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Fits Under Bridge") {
        match_under_bridge = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Doesn't Fit Under Bridge") {
        match_not_under_bridge = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Toppled Own Tower") {
        match_knocked_tower = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match DC :(") {
        match_DC = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Dangerous Driving") {
        match_dangerous_driving = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Steps Over Bridge") {
        match_steps_over_bridge = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match GP :)") {
        match_very_gp = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Not GP :(") {
        match_not_gp = checkboxElem.checked;
    }
    searchChange();
}

function getTeams() {
    if (!(match_feeder || match_stacker || match_speedy || match_tall_lift || match_under_bridge || match_not_under_bridge || match_knocked_tower || match_DC || match_dangerous_driving || match_steps_over_bridge || match_very_gp || match_not_gp)) {
        return teamsUnprocessed;
    }
    let teams = Object.keys(teamsUnprocessed);
    teams=teams.map(Number);
    if (match_feeder) {
        teams = teams.filter(element => feeder_list.includes(element));
    }
    if (match_stacker) {
        teams = teams.filter(element => stacker_list.includes(element));
    }
    if (match_speedy) {
        teams = teams.filter(element => speedy_list.includes(element));
    }
    if (match_tall_lift) {
        teams = teams.filter(element => tall_lift_list.includes(element));
    }
    if (match_under_bridge) {
        teams = teams.filter(element => under_bridge_list.includes(element));
    }
    if (match_not_under_bridge) {
        teams = teams.filter(element => not_under_bridge_list.includes(element));
    }
    if (match_knocked_tower) {
        teams = teams.filter(element => knocked_tower_list.includes(element));
    }
    if (match_DC) {
        teams = teams.filter(element => DC_list.includes(element));
    }
    if (match_dangerous_driving) {
        teams = teams.filter(element => dangerous_driving_list.includes(element));
    }
    if (match_steps_over_bridge) {
        teams = teams.filter(element => steps_over_bridge_list.includes(element));
    }
    if (match_very_gp) {
        teams = teams.filter(element => very_gp_list.includes(element));
    }
    if (match_not_gp) {
        teams = teams.filter(element => not_gp_list.includes(element));
    }
    let teamPairs = {}
    for (let element of teams) {
        teamPairs[element] = teamsUnprocessed[element];
    }
    return teamPairs;
}

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
    var teams = getTeams();
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
        if (count >= 50) {
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


$(document).ready(function () {
    $('#all-filters-toggle').click(toggleAllFilterVisibility);
    $('#all-filters-toggle').mousedown(function () {
        $('#all-filters-toggle').css('color', '#84aaf2');
    });
    $('#all-filters-toggle').mouseup(function () {
        $('#all-filters-toggle').css('color', '');
    });
});

function toggleAllFilterVisibility() {
    if ($('#all-filters').css("display") == "none") {
        $('#all-filters').css("display", "")
        $('#all-filters-toggle').text("\u25BC All Filters \u25BC")
    } else {
        $('#all-filters').css("display", "none")
        $('#all-filters-toggle').text("\u25B2 All Filters \u25B2")
    }
}


searchChange();
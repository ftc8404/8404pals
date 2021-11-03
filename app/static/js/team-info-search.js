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
var detect_element_list = lists[0];
var carousel_list = lists[1];
var terrain_over_list = lists[2];
var terrain_around_list = lists[3];
var fast_freight_list = lists[4];
var high_deposit_list = lists[5];
var cap_list = lists[6];
var dc_list = lists[7];
var very_gp_list = lists[8];
var not_gp_list = lists[9];
var possessive_list = lists[10];
// var gold_list = compData.goldDiv;
// var silicon_list = compData.siliconDiv;


var match_detect_element = false;
var match_carousel = false;
var match_terrain_over = false;
var match_terrain_around = false;
var match_fast_freight = false;
var match_high_deposit = false;
var match_cap = false;
var match_dc = false;
var match_very_gp = false;
var match_not_gp = false;
var match_possessive = false;
// var match_gold = false;
// var match_silicon = false;

function changeFilter(checkboxElem) {
    if (checkboxElem.id == "Match Detect Element") {
        match_detect_element = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Carousel") {
        match_carousel = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Terrain Over") {
        match_terrain_over = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Terrain Around") {
        match_terrain_around = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Fast Freight") {
        match_fast_freight = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match High Deposit") {
        match_high_deposit = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Cap") {
        match_cap = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match DC :(") {
        match_dc = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match GP :)") {
        match_very_gp = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Not GP :(") {
        match_not_gp = checkboxElem.checked;
    }
    if (checkboxElem.id == "Match Possession Penalties") {
        match_possessive = checkboxElem.checked;
    }
    // if (checkboxElem.id == "Match Gold Division") {
    //     match_gold = checkboxElem.checked;
    // }
    // if (checkboxElem.id == "Match Silicon Division") {
    //     match_silicon = checkboxElem.checked;
    // }
    searchChange();
}

function getTeams() {
    // if (!(match_gold || match_silicon || match_detect_element || match_carousel || match_terrain_over || match_terrain_around || match_fast_freight || match_high_deposit || match_cap || match_dc || match_very_gp || match_not_gp || match_possessive)) {
    //     return teamsUnprocessed;
    // }
    if (!( match_detect_element || match_carousel || match_terrain_over || match_terrain_around || match_fast_freight || match_high_deposit || match_cap || match_dc || match_very_gp || match_not_gp || match_possessive)) {
        return teamsUnprocessed;
    }
    let teams = Object.keys(teamsUnprocessed);
    teams=teams.map(Number);
    if (match_detect_element) {
        teams = teams.filter(element => detect_element_list.includes(element));
    }
    if (match_carousel) {
        teams = teams.filter(element => carouselr_list.includes(element));
    }
    if (match_terrain_over) {
        teams = teams.filter(element => terrain_over_list.includes(element));
    }
    if (match_terrain_around) {
        teams = teams.filter(element => terrain_around_list.includes(element));
    }
    if (match_fast_freight) {
        teams = teams.filter(element => fast_freight_list.includes(element));
    }
    if (match_high_deposit) {
        teams = teams.filter(element => high_deposit_list.includes(element));
    }
    if (match_cap) {
        teams = teams.filter(element => cap_list.includes(element));
    }
    if (match_dc) {
        teams = teams.filter(element => dc_list.includes(element));
    }
    if (match_very_gp) {
        teams = teams.filter(element => very_gp_list.includes(element));
    }
    if (match_not_gp) {
        teams = teams.filter(element => not_gp_list.includes(element));
    }
    if (match_possessive) {
        teams = teams.filter(element => possessive_list.includes(element));
    }
    // if (match_gold) {
    //     teams = teams.filter(element => gold_list.includes(element));
    // }
    // if (match_silicon) {
    //     teams = teams.filter(element => silicon_list.includes(element));
    // }
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
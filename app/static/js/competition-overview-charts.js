var Httpreq = new XMLHttpRequest();
// a new request 
Httpreq.open("GET", "/api/competition-overview/", false);
Httpreq.send(null); var compData = JSON.parse(Httpreq.responseText);

var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/team-info/", false);
Httpreq.send(null);
var teamsUnprocessed = JSON.parse(Httpreq.responseText);

Chart.defaults.global.defaultFontColor = '#585858';
Chart.defaults.global.defaultFontColor.defaultFontFamily = "'Source Sans Pro', 'Helvetica', 'sans-serif'";
Chart.defaults.global.defaultFontColor.defaultFontSize = 16;

var allData = compData.allData;
var teamsPreGame = [];
var teamsMatch = [];
// var goldTeamsPreGame = [];
// var siliconTeamsPreGame = [];
// var goldTeamsMatch = [];
// var siliconTeamsMatch = [];


// var goldPreGameDatasets = [{ label: 'Pre-Game Autonomous', data: [], backgroundColor: '#ff6699', stack: 'pre-game' }, { label: 'Pre-Game Tele-Op', data: [], backgroundColor: '#ffcc66', stack: 'pre-game' }];
// var siliconPreGameDatasets = [{ label: 'Pre-Game Autonomous', data: [], backgroundColor: '#ff6699', stack: 'pre-game' }, { label: 'Pre-Game Tele-Op', data: [], backgroundColor: '#ffcc66', stack: 'pre-game' }];
// var goldMatchDatasets = [{ label: 'Match Autonomous', data: [], backgroundColor: '#cc99ff', stack: 'main' }, { label: 'Match Tele-Op', data: [], backgroundColor: '#6699ff', stack: 'main' }];
// var siliconMatchDatasets = [{ label: 'Match Autonomous', data: [], backgroundColor: '#cc99ff', stack: 'main' }, { label: 'Match Tele-Op', data: [], backgroundColor: '#6699ff', stack: 'main' }];

var preGameDatasets = [{ label: 'Pre-Game Autonomous', data: [], backgroundColor: '#ff6699', stack: 'pre-game' }, { label: 'Pre-Game Tele-Op', data: [], backgroundColor: '#ffcc66', stack: 'pre-game' }];
var matchDatasets = [{ label: 'Match Autonomous', data: [], backgroundColor: '#cc99ff', stack: 'main' }, { label: 'Match Tele-Op', data: [], backgroundColor: '#6699ff', stack: 'main' }];

var preGameDataUnsorted = [];
var matchDataUnsorted = [];

var missingPreGameTeams = [];
var missingMatchTeams = [];

// var goldDivisionTeams = compData.goldDiv;
// var siliconDivisionTeams = compData.siliconDiv;


for (let teamNumber in allData) {
    let teamDataRaw = allData[teamNumber];

    if (teamDataRaw[50] == 'N/A') {
        missingPreGameTeams.push(teamNumber)
    }
    else {
        preGameDataUnsorted.push([teamNumber, teamDataRaw[50], teamDataRaw[51]]); // TODO 
    } if (teamDataRaw[53] == 'N/A') {
        missingMatchTeams.push(teamNumber)
    } else {
        matchDataUnsorted.push([teamNumber, teamDataRaw[53], teamDataRaw[54]]); // TODO 
    }
}

preGameDataUnsorted.sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) });
matchDataUnsorted.sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) });

for (let i = 0; i < missingPreGameTeams.length; i++) {
    preGameDataUnsorted.push([missingPreGameTeams[i], 0, 0]);
}

for (let i = 0; i < missingMatchTeams.length; i++) {
    matchDataUnsorted.push([missingMatchTeams[i], 0, 0]);
}


// for (let i = 0; i < preGameDataUnsorted.length; i++) {
//     let entry = preGameDataUnsorted[i];
//     teamNumber = parseInt(entry[0])
//     if (goldDivisionTeams.indexOf(teamNumber) > -1) {
//         goldTeamsPreGame.push(entry[0]);
//         goldPreGameDatasets[0].data.push(entry[1]);
//         goldPreGameDatasets[1].data.push(entry[2]);
//     } else {
//         siliconTeamsPreGame.push(entry[0]);
//         siliconPreGameDatasets[0].data.push(entry[1]);
//         siliconPreGameDatasets[1].data.push(entry[2]);
//     }
// }

for (let i = 0; i < preGameDataUnsorted.length; i++) {
    let entry = preGameDataUnsorted[i];
    teamNumber = parseInt(entry[0])
    teamsPreGame.push(entry[0])
    preGameDatasets[0].data.push(entry[1]);
    preGameDatasets[1].data.push(entry[2]);
}

// for (let i = 0; i < matchDataUnsorted.length; i++) {
//     let entry = matchDataUnsorted[i];
//     teamNumber = parseInt(entry[0])
//     if (goldDivisionTeams.indexOf(teamNumber) > -1) {
//         goldMatchDatasets[0].data.push(entry[1]);
//         goldMatchDatasets[1].data.push(entry[2]);
//     } else {
//         siliconMatchDatasets[0].data.push(entry[1]);
//         siliconMatchDatasets[1].data.push(entry[2]);
//     }
// }

for (let i = 0; i < matchDataUnsorted.length; i++) {
    let entry = matchDataUnsorted[i];
    teamNumber = parseInt(entry[0])
    teamsMatch.push(entry[0])
    matchDatasets[0].data.push(entry[1]);
    matchDatasets[1].data.push(entry[2]);
}

function updateChartScope() {
    // if ($('input[name=chart-scope]:checked').val() == 'pre-game-gold') {
    //     chartDispPreGameScouting("gold");
    // }
    // else if ($('input[name=chart-scope]:checked').val() == 'pre-game-silicon') {
    //     chartDispPreGameScouting("silicon");
    // }
    // else if ($('input[name=chart-scope]:checked').val() == 'match-gold') {
    //     chartDispMatchScouting("gold");
    // } else {
    //     chartDispMatchScouting("silicon");
    // }

    if ($('input[name=chart-scope]:checked').val() == 'pre-game') {
        chartDispPreGameScouting("none");
    }
    else if ($('input[name=chart-scope]:checked').val() == 'match') {
        chartDispMatchScouting("none");
    }
}

function chartDispPreGameScouting(division) {
    // if (division == "gold") {
    //     chart.data.labels = goldTeamsPreGame;
    //     chart.data.datasets = goldPreGameDatasets;
    // }
    // if (division == "silicon") {
    //     chart.data.labels = siliconTeamsPreGame;
    //     chart.data.datasets = siliconPreGameDatasets;
    // }
    if (division == "none") {
        chart.data.labels = teamsPreGame;
        chart.data.datasets = preGameDatasets;
    }
    chart.options.scales.xAxes[0].stacked = true;
    chart.options.scales.yAxes[0].stacked = true;
    chart.update();
}

function chartDispMatchScouting(division) {
    // if (division == "gold") {
    //     chart.data.labels = goldTeamsPreGame;
    //     chart.data.datasets = goldMatchDatasets;
    // }
    // if (division == "silicon") {
    //     chart.data.labels = siliconTeamsPreGame;
    //     chart.data.datasets = siliconMatchDatasets;
    // }
    if (division == "none") {
        chart.data.labels = teamsMatch;
        chart.data.datasets = matchDatasets;
    }
    chart.options.scales.xAxes[0].stacked = true;
    chart.options.scales.yAxes[0].stacked = true;
    chart.update();
}

function chartDispAllScouting() {
    chart.data.datasets = allDataSets;
    chart.options.scales.xAxes[0].stacked = false;
    chart.options.scales.yAxes[0].stacked = false;
    chart.update();
}

var ctx = document.getElementById("chart").getContext('2d');
var chart = new Chart(ctx, {
    type: 'horizontalBar',
    data: { labels: [], datasets: [] },
    options: {
        scales: {
            xAxes: [{ stacked: true, ticks: { beginAtZero: true } }],
            yAxes: [{ stacked: true }]
        },
        aspectRatio: null,
        maintainAspectRatio: false
    }
});

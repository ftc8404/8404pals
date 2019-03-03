var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/competition-overview/", false);
Httpreq.send(null);
var compData = JSON.parse(Httpreq.responseText);

Chart.defaults.global.defaultFontColor = '#585858';
Chart.defaults.global.defaultFontColor.defaultFontFamily = "'Source Sans Pro', 'Helvetica', 'sans-serif'";
Chart.defaults.global.defaultFontColor.defaultFontSize = 16;

var allData = compData.allData;
var allTeamsPreGame = [];
var allTeamsMatch = [];

var allData2 = compData.allData2;
var allTeamsPreGame2 = [];
var allTeamsMatch2 = [];

var preGameDatasets = [{ label: 'Pre-Game Autonomous', data: [], backgroundColor: '#ff6699', stack: 'pre-game' }, { label: 'Pre-Game Tele-Op', data: [], backgroundColor: '#ffcc66', stack: 'pre-game' }];
var matchDatasets = [{ label: 'Match Autonomous', data: [], backgroundColor: '#cc99ff', stack: 'main' }, { label: 'Match Tele-Op', data: [], backgroundColor: '#6699ff', stack: 'main' }];

var preGameDatasets2 = [{ label: 'Pre-Game Autonomous', data: [], backgroundColor: '#ff6699', stack: 'pre-game' }, { label: 'Pre-Game Tele-Op', data: [], backgroundColor: '#ffcc66', stack: 'pre-game' }];
var matchDatasets2 = [{ label: 'Match Autonomous', data: [], backgroundColor: '#cc99ff', stack: 'main' }, { label: 'Match Tele-Op', data: [], backgroundColor: '#6699ff', stack: 'main' }];

var preGameDataUnsorted = [];
var matchDataUnsorted = [];

var missingPreGameTeams = [];
var missingMatchTeams = [];

var preGameDataUnsorted2 = [];
var matchDataUnsorted2 = [];

var missingPreGameTeams2 = [];
var missingMatchTeams2 = [];

for (let teamNumber in allData) {

    let teamDataRaw = allData[teamNumber];
    if (teamDataRaw[32] == 'N/A') {
        missingPreGameTeams.push(teamNumber)
    } else {
        preGameDataUnsorted.push([teamNumber, Math.max(teamDataRaw[29], teamDataRaw[30]), teamDataRaw[32]]);
    }

    if (teamDataRaw[35] == 'N/A') {
        missingMatchTeams.push(teamNumber)
    } else {
        matchDataUnsorted.push([teamNumber, teamDataRaw[34], teamDataRaw[35]]);
    }
}

for (let teamNumber in allData2) {

    let teamDataRaw = allData2[teamNumber];
    if (teamDataRaw[32] == 'N/A') {
        missingPreGameTeams2.push(teamNumber)
    } else {
        preGameDataUnsorted2.push([teamNumber, Math.max(teamDataRaw[29], teamDataRaw[30]), teamDataRaw[32]]);
    }

    if (teamDataRaw[35] == 'N/A') {
        missingMatchTeams2.push(teamNumber)
    } else {
        matchDataUnsorted2.push([teamNumber, teamDataRaw[34], teamDataRaw[35]]);
    }
}

preGameDataUnsorted.sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) });
matchDataUnsorted.sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) });

preGameDataUnsorted2.sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) });
matchDataUnsorted2.sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) });

for (let i = 0; i < missingPreGameTeams.length; i++) {
    preGameDataUnsorted.push([missingPreGameTeams[i], 0, 0]);
}

for (let i = 0; i < missingMatchTeams.length; i++) {
    matchDataUnsorted.push([missingMatchTeams[i], 0, 0]);
}

for (let i = 0; i < preGameDataUnsorted.length; i++) {
    let entry = preGameDataUnsorted[i];
    allTeamsPreGame.push(entry[0]);
    preGameDatasets[0].data.push(entry[1]);
    preGameDatasets[1].data.push(entry[2]);
}

for (let i = 0; i < matchDataUnsorted.length; i++) {
    let entry = matchDataUnsorted[i];
    allTeamsMatch.push(entry[0]);
    matchDatasets[0].data.push(entry[1]);
    matchDatasets[1].data.push(entry[2]);
}


for (let i = 0; i < missingPreGameTeams2.length; i++) {
    preGameDataUnsorted2.push([missingPreGameTeams2[i], 0, 0]);
}

for (let i = 0; i < missingMatchTeams2.length; i++) {
    matchDataUnsorted2.push([missingMatchTeams2[i], 0, 0]);
}

for (let i = 0; i < preGameDataUnsorted2.length; i++) {
    let entry = preGameDataUnsorted2[i];
    allTeamsPreGame2.push(entry[0]);
    preGameDatasets2[0].data.push(entry[1]);
    preGameDatasets2[1].data.push(entry[2]);
}

for (let i = 0; i < matchDataUnsorted2.length; i++) {
    let entry = matchDataUnsorted2[i];
    allTeamsMatch2.push(entry[0]);
    matchDatasets2[0].data.push(entry[1]);
    matchDatasets2[1].data.push(entry[2]);
}


function updateChartScope() {
    if ($('input[name=chart-scope]:checked').val() == 'pre-game') {
        chartDispPreGameScouting();
    } else {
        chartDispMatchScouting();
    }
}


function chartDispPreGameScouting() {
    chart.data.labels = allTeamsPreGame;
    chart.data.datasets = preGameDatasets;
    chart.options.scales.xAxes[0].stacked = true;
    chart.options.scales.yAxes[0].stacked = true;
    chart.update();

    chart2.data.labels = allTeamsPreGame2;
    chart2.data.datasets = preGameDatasets2;
    chart2.options.scales.xAxes[0].stacked = true;
    chart2.options.scales.yAxes[0].stacked = true;
    chart2.update();
}

function chartDispMatchScouting() {
    chart.data.labels = allTeamsMatch;
    chart.data.datasets = matchDatasets;
    chart.options.scales.xAxes[0].stacked = true;
    chart.options.scales.yAxes[0].stacked = true;
    chart.update();

    chart2.data.labels = allTeamsMatch2;
    chart2.data.datasets = matchDatasets2;
    chart2.options.scales.xAxes[0].stacked = true;
    chart2.options.scales.yAxes[0].stacked = true;
    chart2.update();
}

function chartDispAllScouting() {
    chart.data.datasets = allDataSets;
    chart.options.scales.xAxes[0].stacked = false;
    chart.options.scales.yAxes[0].stacked = false;
    chart.update();

    chart2.data.datasets = allDataSets2;
    chart2.options.scales.xAxes[0].stacked = false;
    chart2.options.scales.yAxes[0].stacked = false;
    chart2.update();
}


var ctx = document.getElementById("chart").getContext('2d');
var ctx2 = document.getElementById("chart2").getContext('2d');


var chart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        scales: {
            xAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true
                }
            }],
            yAxes: [{
                stacked: true
            }]
        },
        aspectRatio: null,
        maintainAspectRatio: false
    }
});

var chart2 = new Chart(ctx2, {
    type: 'horizontalBar',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        scales: {
            xAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true
                }
            }],
            yAxes: [{
                stacked: true
            }]
        },
        aspectRatio: null,
        maintainAspectRatio: false
    }
});
var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/competition-overview-data", false);
Httpreq.send(null);
var compData = JSON.parse(Httpreq.responseText);

Chart.defaults.global.defaultFontColor = '#585858';
Chart.defaults.global.defaultFontColor.defaultFontFamily = "'Source Sans Pro', 'Helvetica', 'sans-serif'";
Chart.defaults.global.defaultFontColor.defaultFontSize = 16;

var allData = compData.allData;
var allTeams = [];
var preGameDatasets = [{ label: 'Pre-Game Autonomous', data: [], backgroundColor: '#ff6699', stack: 'pre-game' }, { label: 'Pre-Game Tele-Op', data: [], backgroundColor: '#ffcc66', stack: 'pre-game' }];
var matchDatasets = [{ label: 'Match Autonomous', data: [], backgroundColor: '#cc99ff', stack: 'main' }, { label: 'Match Tele-Op', data: [], backgroundColor: '#6699ff', stack: 'main' }];
for (let teamNumber in allData) {
    allTeams.push(teamNumber);
    let teamDataRaw = allData[teamNumber];

    preGameDatasets[0].data.push(Math.max(teamDataRaw[29], teamDataRaw[30]));
    preGameDatasets[1].data.push(teamDataRaw[32]);

    matchDatasets[0].data.push(teamDataRaw[34]);
    matchDatasets[1].data.push(teamDataRaw[35]);
}

function updateChartScope() {
    if ($('input[name=chart-scope]:checked').val() == 'pre-game') {
        chartDispPreGameScouting();
    } else {
        chartDispMatchScouting();
    }
}


function chartDispPreGameScouting() {
    chart.data.datasets = preGameDatasets;
    chart.options.scales.xAxes[0].stacked = true;
    chart.options.scales.yAxes[0].stacked = true;
    chart.update();
}

function chartDispMatchScouting() {
    chart.data.datasets = matchDatasets;
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
    data: {
        labels: allTeams,
        datasets: []
    },
    options: {
        scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        aspectRatio: null,
        maintainAspectRatio: false
    }
});
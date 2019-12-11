var teamNumber = window.location.pathname.substring(11);
if (teamNumber.substring(teamNumber.length - 1) == '/') {
    teamNumber = teamNumber.substring(0, teamNumber.length - 1);
}
teamNumber = parseInt(teamNumber);

var HttpreqTeam = new XMLHttpRequest(); // a new request
HttpreqTeam.open("GET", "/api/team-info/" + teamNumber + "/", false);
HttpreqTeam.send(null);
var teamData = JSON.parse(HttpreqTeam.responseText);

var HttpreqComp = new XMLHttpRequest(); // a new request
HttpreqComp.open("GET", "/api/competition-overview/", false);
HttpreqComp.send(null);
var compData = JSON.parse(HttpreqComp.responseText);

Chart.defaults.global.defaultFontColor = '#585858';
Chart.defaults.global.defaultFontColor.defaultFontFamily = "'Source Sans Pro', 'Helvetica', 'sans-serif'";
Chart.defaults.global.defaultFontColor.defaultFontSize = 16;

var compInfo = teamData.compInfo;
var matches = compInfo.matches;

var allData = compData.allData;
var curTeamData = allData[teamNumber];

var perfLabels = [
    'Auton Stones', 'Auton Skystone', 'Auton Other',
    'Tele-Op Stones', 'Tele-Op Bonuses', 'Tele-Op Other'
]
var perfColors = [
    '#00ff99', '#66ff66', '#99ffcc',
    '#ffcc66', '#ff9933', '#ffcc99'
];

var perfData = []
if (curTeamData[4] > 0) {
    perfData.push(curTeamData[2] * 6);
} else {
    perfData.push(curTeamData[2] * 2);
}
perfData.push(curTeamData[3] * Math.min(curTeamData[2], 2) * 8);
perfData.push(curTeamData[5] * 10 + curTeamData[6] * 5);

if (curTeamData[8] > 0) {
    perfData.push(curTeamData[7] * 2);
} else {
    perfData.push(curTeamData[7]);
}
var bonus = curTeamData[8] * 2;
if (curTeamData[9] > 0) {
    bonus += curTeamData[8] + 5;
}
perfData.push(bonus);
perfData.push(curTeamData[10] * 15 + curTeamData[11] * 5);


var ctx = document.getElementById("chart-perf-pre-game").getContext('2d');
var perfChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: perfData,
            backgroundColor: perfColors
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: perfLabels
    },
    options: {
        aspectRatio: 1.5,
        maintainAspectRatio: true
    }
});

var perfLabels = [
    'Auton Stones', 'Auton Skystone', 'Auton Other',
    'Tele-Op Stones', 'Tele-Op Bonuses', 'Tele-Op Other'
]
var perfColors = [
    '#00ff99', '#66ff66', '#99ffcc',
    '#ffcc66', '#ff9933', '#ffcc99'
];

var perfData = []
if (curTeamData[14] > 0) {
    perfData.push(curTeamData[12] * 6);
} else {
    perfData.push(curTeamData[12] * 2);
}
perfData.push(curTeamData[13] * Math.min(curTeamData[12], 2) * 8);
perfData.push(curTeamData[15] * 10 + curTeamData[16] * 5);

if (curTeamData[18] > 0) {
    perfData.push(curTeamData[17] * 2);
} else {
    perfData.push(curTeamData[17]);
}
var bonus = curTeamData[18] * 2;
if (curTeamData[19] > 0) {
    bonus += curTeamData[18] + 5;
}
perfData.push(bonus);
perfData.push(curTeamData[20] * 15 + curTeamData[21] * 5);

var ctx = document.getElementById("chart-perf-match").getContext('2d');
var perfChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: perfData,
            backgroundColor: perfColors
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: perfLabels
    },
    options: {
        aspectRatio: 1.5,
        maintainAspectRatio: true
    }
});

for (let i = 0; i < matches.length; i++) {
    let match = matches[i];
    let matchNumber = match.number;

    let teamGraphOrder = [teamNumber, match.alliance, match.opponent1, match.opponent2];
    let preGameScores = [];
    let matchScores = [];

    for (let j = 0; j < 4; j++) {
        rowTeamNumber = teamGraphOrder[j]
        let teamDataRaw = allData[rowTeamNumber];
        preGameScores.push(teamDataRaw[24]);
        matchScores.push(teamDataRaw[27]);
    }

    let ctx = document.getElementById("chart-" + matchNumber).getContext('2d');
    let backgroundColorSets;
    if (match.color == 'Red') {
        backgroundColorSets = [[
            'rgba(255, 99, 132, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(54, 162, 235, 1)'
        ], [
            'rgba(255, 99, 132, 0.4',
            'rgba(255, 99, 132, 0.4)',
            'rgba(54, 162, 235, 0.4)',
            'rgba(54, 162, 235, 0.4)'
        ]];
    } else {
        backgroundColorSets = [[
            'rgba(54, 162, 235, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(255, 99, 132, 1)'
        ], [
            'rgba(54, 162, 235, 0.4)',
            'rgba(54, 162, 235, 0.4)',
            'rgba(255, 99, 132, 0.4',
            'rgba(255, 99, 132, 0.4)'
        ]];
    }

    let chart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: teamGraphOrder,
            datasets: [{
                label: 'Avg. Match Score',
                data: matchScores,
                backgroundColor: backgroundColorSets[0]
            },
            {
                label: 'Pre-Game Scouting',
                data: preGameScores,
                backgroundColor: backgroundColorSets[1]
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}
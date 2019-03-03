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
    'Land', 'Sample', 'Marker', 'Park',
    'Minerals', 'End-Game'
]
var perfColors = [
    '#00ff99', '#99ffcc', '#66ff66', '#ccff99',
    '#ffcc66', '#ffcc99'
];

var perfData = []
var offset = 0;
if (curTeamData[30] > curTeamData[29]) {
    offset = 1;
}
perfData.push(curTeamData[2 + offset] * 30);
perfData.push(Math.max(curTeamData[4 + offset] * 25, curTeamData[6 + offset] * 50));
perfData.push(curTeamData[8 + offset] * 15);
perfData.push(curTeamData[10 + offset] * 10);
var minerals = curTeamData[12];
if (curTeamData[17]) {
    minerals *= 5;
} else if (curTeamData[18]) {
    minerals *= 2;
} else {
    minerals = 0;
}
perfData.push(minerals);

var endGame = 15;
if (curTeamData[19] != 'N/A' && curTeamData[19]) {
    endGame = 50;
} else if (curTeamData[20] != 'N/A' && curTeamData[20]) {
    endGame = 25;
}
perfData.push(endGame);

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
    'Land', 'Sample', 'Marker', 'Park',
    'Minerals Lander', 'Minerals Depot', 'End-Game'
]
var perfColors = [
    '#00ff99', '#99ffcc', '#66ff66', '#ccff99',
    '#ffcc66', '#ff9933', '#ffcc99'
];

var perfData = []
perfData.push(curTeamData[21] * 30);
perfData.push(Math.max(curTeamData[22] * 25, curTeamData[23] * 50));
perfData.push(curTeamData[24] * 15);
perfData.push(curTeamData[25] * 10);
perfData.push(curTeamData[26] * 5);
perfData.push(curTeamData[27] * 2);
perfData.push(curTeamData[28] * 1);

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
        preGameScores.push(Math.max(teamDataRaw[29], teamDataRaw[30]) + teamDataRaw[32]);
        matchScores.push(teamDataRaw[34] + teamDataRaw[35]);
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
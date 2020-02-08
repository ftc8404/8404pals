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
];
var perfColors = [
    '#00ff99', '#66ff66', '#99ffcc',
    '#ffcc66', '#ff9933', '#ffcc99'
];

var perfData = []

// Auton scoring points
perfData.push(curTeamData[2] * 2);
perfData.push(curTeamData[3] * 8);
perfData.push(curTeamData[4] * 4 + curTeamData[5] * 10 + curTeamData[6] * 5);

// Teleop scoring poits
perfData.push(curTeamData[7] * 2 + curTeamData[8] * 2);

var bonus = 0;
if (curTeamData[9] > 0) {
    bonus += curTeamData[8] + 5;
}
perfData.push(bonus)
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

var perfData = [];

// Auton scoring points
perfData.push(curTeamData[12] * 2);
perfData.push(curTeamData[13] * 8);
perfData.push(curTeamData[14] * 4 + curTeamData[15] * 10 + curTeamData[16] * 5);

// Teleop scoring poits
var highestStack = 0;
var StackList = [curTeamData[18], curTeamData[19], curTeamData[20], curTeamData[21]];
for (let i = 0; i < StackList.length; i++) {
    if (StackList[i] > highestStack) {
        highestStack = StackList[i];
    }
}
perfData.push(curTeamData[17] * 2 + highestStack * 2);

var bonus = 0;
var capList = [curTeamData[22], curTeamData[23], curTeamData[24], curTeamData[25]]; 
var capIndex = 5;
for (let i = 0; i < capList.length; i++) {
    if (capList[i] == true) {
        capIndex = i;
    }
}
if (capIndex != 5) {
    bonus += StackList[capIndex] + 5;
}
perfData.push(bonus)

// var teleopOther = 0;
// if (curTeamData[26]) {
//     teleopOther += 15;
// }
// if (curTeamData[27]) {
//     teleopOther += 5;
// }
// perfData.push(teleopOther);
if (curTeamData[26] && curTeamData[27]) {
    perfData.push(curTeamData[26]  * 15 + curTeamData[27] * 5);
}

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
        preGameScores.push(teamDataRaw[40]);
        matchScores.push(teamDataRaw[43]);
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
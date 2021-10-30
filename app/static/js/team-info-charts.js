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
    'Auton Frieght', 'Auton Duck', 'Auton Other',
    'Tele-Op Frieght', 'Tele-Op Duck', 'Tele-Op Other'
];
var perfColors = [
    '#00ff99', '#66ff66', '#99ffcc',
    '#ffcc66', '#ff9933', '#ffcc99'
];

var perfData = []

// Auton scoring points

// Count points from freight
var auton_freight_score = (curTeamData[5] * 2 ) + (curTeamData[6] * 6);

// Count points from ducks and detection
var auton_duck_score = (curTeamData[2] * 10) + (curTeamData[7] * 10) + (curTeamData[8] *20)

// Count parking points
var auton_park = (curTeamData[3] * 6) + (curTeamData[4] * 10);

perfData.push(auton_freight_score);
perfData.push(auton_duck_score);
perfData.push(auton_park);

// Teleop scoring poits

// Count points from freight
var teleop_freight_score = (curTeamData[9] * 1 ) + (curTeamData[10] * 2) + (curTeamData[11] * 4) + (curTeamData[12] * 6) + (curTeamData[13] * 4);

// Count points from ducks and detection
var teleop_duck_score = (curTeamData[14] * 6) + (curTeamData[15] * 20) + (curTeamData[16] * 10)

// Count parking points
var teleop_park = (curTeamData[17] * 6) + (curTeamData[18] * 15);

perfData.push(teleop_freight_score);
perfData.push(teleop_duck_score);
perfData.push(teleop_park);



var ctx = document.getElementById("chart-perf-pre-game").getContext('2d');
var perfChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        datasets: [{
            data: perfData,
            backgroundColor: perfColors,
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: perfLabels
    },
    options: {
        legend: {
            display: false
        },
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

// Count points from freight
var auton_freight_score = (curTeamData[24] * 2 ) + (curTeamData[25] * 6);

// Count points from ducks and detection
var auton_duck_score = (curTeamData[19] * 10) + (curTeamData[26] * 10) + (curTeamData[27] *20)

// Count parking points
var auton_park = (curTeamData[20] * 3) + (curTeamData[21] * 6) + (curTeamData[22] * 5) + (curTeamData[23] * 10);

perfData.push(auton_freight_score);
perfData.push(auton_duck_score);
perfData.push(auton_park);

// Teleop scoring poits

// Count points from freight
var teleop_freight_score = (curTeamData[28] * 1 ) + (curTeamData[29] * 2) + (curTeamData[30] * 4) + (curTeamData[31] * 6) + (curTeamData[32] * 4);

// Count points from ducks and detection
var teleop_duck_score = (curTeamData[33] * 6) + (curTeamData[34] * 20) + (curTeamData[35] * 10)

// Count parking points
var teleop_park = (curTeamData[36] * 3) + (curTeamData[37] * 6) + (curTeamData[38] * 15);

perfData.push(teleop_freight_score);
perfData.push(teleop_duck_score);
perfData.push(teleop_park);

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
    type: 'horizontalBar',
    data: {
        datasets: [{
            data: perfData,
            backgroundColor: perfColors
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: perfLabels
    },
    options: {
        legend: {
            display: false
        },
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
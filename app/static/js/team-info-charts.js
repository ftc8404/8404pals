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
HttpreqComp.open("GET", "/api/competition-overview-data", false);
HttpreqComp.send(null);
var compData = JSON.parse(HttpreqComp.responseText);

Chart.defaults.global.defaultFontColor = '#585858';
Chart.defaults.global.defaultFontColor.defaultFontFamily = "'Source Sans Pro', 'Helvetica', 'sans-serif'";
Chart.defaults.global.defaultFontColor.defaultFontSize = 16;

var compInfo = teamData.compInfo;
var matches = compInfo.matches;

var allData = compData.allData;

for (let i = 0; i < matches.length; i++) {
    let match = matches[i];
    let matchNumber = match.number;

    let teamGraphOrder = [teamNumber, match.alliance, match.opponent1, match.opponent2];
    let preGameScores = [];
    let matchScores = [];

    for (let j = 0; j < 4; j++) {
        rowTeamNumber = teamGraphOrder[j]
        let teamDataRaw = allData[rowTeamNumber];
        preGameScores.push(Math.max(teamDataRaw[28], teamDataRaw[29]) + teamDataRaw[31]);
        matchScores.push(teamDataRaw[33] + teamDataRaw[34]);
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
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}
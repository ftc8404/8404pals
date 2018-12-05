var teamNumber = window.location.pathname.substring(10);
if (teamNumber.substring(teamNumber.length - 1) == '/') {
    teamNumber = teamNumber.substring(0, teamNumber.length - 1);
}
teamNumber = parseInt(teamNumber);

var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET", "/api/team-info/" + teamNumber, false);
Httpreq.send(null);
var teamData = JSON.parse(Httpreq.responseText);

Chart.defaults.global.defaultFontColor = '#585858';
Chart.defaults.global.defaultFontColor.defaultFontFamily = "'Source Sans Pro', 'Helvetica', 'sans-serif'";
Chart.defaults.global.defaultFontColor.defaultFontSize = 16;

var compInfo = teamData.compInfo;
var matches = compInfo.matches;

for (var match in matches) {
    matchNumber = match.number;
    var ctx = document.getElementById("chart-" + matchNumber).getContext('2d');

    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [0, 1, 2],
            datasets: [1,2,3]
        },
        options: {
            scales: {
                xAxes: [{
                    stacked: false
                }],
                yAxes: [{
                    stacked: false,
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            aspectRatio: null,
            maintainAspectRatio: false
        }
    });
}
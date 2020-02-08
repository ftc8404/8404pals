var match_under_bridge = true;
var match_not_under_bridge = true;
var match_feeder = true;
var match_stacker = true;
var match_very_gp = true;
var match_not_gp = true;
var match_steps_over_bridge = true;
var match_tall_lift = true;
var match_DC = true;
var match_speedy = true;



$(document).ready(function () {
    $('#other').css('padding-bottom', '4em');
    $("[id='Overall Match Total Score']").css('padding-bottom', '4em');
    setupFilters();
    $('#main-filters-toggle').click();
    $('#other').click();
    $('#chart-toggle').click();
    $('#table-toggle').click();

    updateChartScope();
});

function setupFilters() {
    $('#all-filters-toggle').click(toggleAllFilterVisibility);
    $('#all-filters-toggle').mousedown(function () {
        $('#all-filters-toggle').css('color', '#84aaf2');
    });
    $('#all-filters-toggle').mouseup(function () {
        $('#all-filters-toggle').css('color', '');
    });

    $('#chart-toggle').click(toggleChartVisibility);
    $('#chart-toggle').mousedown(function () {
        $('#chart-toggle').css('color', '#84aaf2');
    });
    $('#chart-toggle').mouseup(function () {
        $('#chart-toggle').css('color', '');
    });

    $('#table-toggle').click(toggleTableVisibility);
    $('#table-toggle').mousedown(function () {
        $('#table-toggle').css('color', '#84aaf2');
    });
    $('#table-toggle').mouseup(function () {
        $('#table-toggle').css('color', '');
    });
}


function toggleAllFilterVisibility() {
    if ($('#all-filters').css("display") == "none") {
        $('#all-filters').css("display", "")
        $('#all-filters-toggle').text("\u25BC All Filters \u25BC")
    } else {
        $('#all-filters').css("display", "none")
        $('#all-filters-toggle').text("\u25B2 All Filters \u25B2")
    }
}

function toggleChartVisibility() {
    if ($('#chart-parent').css("display") == "none") {
        $('#chart-parent').css("display", "block")
        $('#chart-toggle').text("\u25BC Chart \u25BC")
    } else {
        $('#chart-parent').css("display", "none")
        $('#chart-toggle').text("\u25B2 Chart \u25B2")
    }
}

function toggleTableVisibility() {
    if ($('#table-parent').css("display") == "none") {
        $('#table-parent').css("display", "block")
        $('#table-toggle').text("\u25BC Scouting Data \u25BC")
    } else {
        $('#table-parent').css("display", "none")
        $('#table-toggle').text("\u25B2 Scouting Data \u25B2")
    }
}

function changeFilter(checkboxElem) {
    changeVisibility(checkboxElem.id, checkboxElem.checked)
    if(checkboxElem.id=="Match Under Bridge" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Not Under Bridge" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Feeder" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Stacker" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Very Gp" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Not Gp" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Steps Over Bridge" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Tall Lift" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Dc" && !checkboxElem.checked){
        match_under_bridge = false;
    }
    if(checkboxElem.id=="Match Speedy" && !checkboxElem.checked){
        match_under_bridge = false;
    }
}

function changeVisibility(columnName, isVisible) {
    var filterElems = document.getElementsByClassName('filter-' + columnName)
    if (isVisible) {
        for (var i = 0; i < filterElems.length; i++) {
            filterElems[i].style.display = ''
        }
    } else {
        for (var i = 0; i < filterElems.length; i++) {
            filterElems[i].style.display = 'none'
        }
    }
}
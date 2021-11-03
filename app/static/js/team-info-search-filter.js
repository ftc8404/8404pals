var match_detect_element = true;
var match_carousel = true;
var match_terrain_over = true;
var match_terrain_around = true;
var match_fast_freight = true;
var match_high_deposit = true;
var match_cap = true;
var match_dc = true;
var match_very_gp = true;
var match_not_gp = true;
var match_possessive = true;


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
    if(checkboxElem.id=="Match Detect Element" && !checkboxElem.checked){
        match_detect_element = false;
    }
    if(checkboxElem.id=="Match Carousel" && !checkboxElem.checked){
        match_carousel = false;
    }
    if(checkboxElem.id=="Match Terrain Over" && !checkboxElem.checked){
        match_terrain_over = false;
    }
    if(checkboxElem.id=="Match Terrain Around" && !checkboxElem.checked){
        match_terrain_around = false;
    }
    if(checkboxElem.id=="Match Fast Freight" && !checkboxElem.checked){
        match_fast_freight = false;
    }
    if(checkboxElem.id=="Match High Deposit" && !checkboxElem.checked){
        match_not_under_bridge = false;
    }
    if(checkboxElem.id=="Match Cap" && !checkboxElem.checked){
        match_knocked_tower = false;
    }
    if(checkboxElem.id=="Match DC :(" && !checkboxElem.checked){
        match_dc = false;
    }
    if(checkboxElem.id=="Match GP :)" && !checkboxElem.checked){
        match_very_gp = false;
    }
    if(checkboxElem.id=="Match Not GP :(" && !checkboxElem.checked){
        match_not_gp = false;
    }
    if(checkboxElem.id=="Match Possession Penalties" && !checkboxElem.checked){
        match_possessive = false;
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
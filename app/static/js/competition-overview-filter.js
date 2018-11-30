$(document).ready(function () {
    $('#other').css('padding-bottom', '4em');
    $("[id='Overall Total Score']").css('padding-bottom', '4em');
    setupFilters();
    $('#main-filters-toggle').click();
    $('#other').click();
    $('#chart-toggle').click();
    $('#table-toggle').click();
});

function setupFilters() {
    $('#all-filters-toggle').click(toggleAllFilterVisibility);
    $('#all-filters-toggle').mousedown(function () {
        $('#all-filters-toggle').css('color', '#84aaf2');
    });
    $('#all-filters-toggle').mouseup(function () {
        $('#all-filters-toggle').css('color', '');
    });

    $('#main-filters-toggle').click(toggleMainFilterVisibility);
    $('#main-filters-toggle').mousedown(function () {
        $('#main-filters-toggle').css('color', '#84aaf2');
    });
    $('#main-filters-toggle').mouseup(function () {
        $('#main-filters-toggle').css('color', '');
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

    updateChartScope();
}

var viewPreGameData = true;
var viewMatchPerformanceData = true;
var viewOtherData = true;

function toggleTheoreticalVisibility(checkboxElem) {
    viewPreGameData = checkboxElem.checked;
    updateChartScope();
    var inputs = document.getElementById('all-filters').getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].id.substr(0, 11) == 'Theoretical') {
            if (inputs[i].checked != checkboxElem.checked) {
                inputs[i].checked = checkboxElem.checked;
                changeFilter(inputs[i]);
            }
        }
    }
}

function toggleMatchPerformanceVisibility(checkboxElem) {
    viewMatchPerformanceData = checkboxElem.checked;
    updateChartScope();
    var inputs = document.getElementById('all-filters').getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].id.substr(0, 7) == 'Overall') {
            if (inputs[i].checked != checkboxElem.checked) {
                inputs[i].checked = checkboxElem.checked;
                changeFilter(inputs[i]);
            }
        }
    }
}

function toggleOtherVisibility(checkboxElem) {
    viewOtherData = checkboxElem.checked;
    updateChartScope();
    var inputs = document.getElementById('all-filters').getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].id.substr(0, 11) != 'Theoretical' && inputs[i].id.substr(0, 7) != 'Overall') {
            if (inputs[i].checked != checkboxElem.checked) {
                inputs[i].checked = checkboxElem.checked;
                changeFilter(inputs[i]);
            }
        }
    }
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

function toggleMainFilterVisibility() {
    if ($('#main-filters').css("display") == "none") {
        $('#main-filters').css("display", "")
        $('#main-filters-toggle').text("\u25BC Main Filters \u25BC")
    } else {
        $('#main-filters').css("display", "none")
        $('#main-filters-toggle').text("\u25B2 Main Filters \u25B2")
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
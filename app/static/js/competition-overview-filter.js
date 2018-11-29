window.onload = function () {
    setupFilters();
}

function setupFilters() {
    
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
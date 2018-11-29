function changeFilter(checkboxElem) {
    var filterElems = document.getElementsByClassName('filter-' + checkboxElem.id)
    if (checkboxElem.checked) {
        for (var i = 0; i < filterElems.length; i++) {
            filterElems[i].style.display = ''
        }
    } else {
        for (var i = 0; i < filterElems.length; i++) {
            filterElems[i].style.display = 'none'
        }
    }
}
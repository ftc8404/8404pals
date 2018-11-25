var formChanged = false;

document.getElementById("team_number").addEventListener("focusout", teamNumberFocusOut);

function teamNumberFocusOut() {
    if(!formChanged){
        
    }
}

var formElements = document.getElementsByTagName("input");

for (var i = 0, element; element = formElements[i++];) {
    if (element.name != "team_number") {
        element.addEventListener("change", fieldChange);
    }
}

function fieldChange() {
    formChanged = true;
    alert("other change");
}
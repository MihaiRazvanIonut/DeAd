isAsideShown = true;

function toggleAside() {
    if (isAsideShown == true) {
        document.getElementById("aside-info").setAttribute("class", "hidden-aside");
        isAsideShown = false;
    } else {
        document.getElementById("aside-info").setAttribute("class", "shown-aside");
        isAsideShown = true;
    }
}
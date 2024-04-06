isNavShown = true;

function toggleNav() {
    if (isNavShown == true) {
        document.getElementById("page-nav").setAttribute("class", "hidden-nav");
        isNavShown = false;
    } else {
        document.getElementById("page-nav").setAttribute("class", "shown-nav");
        isNavShown = true;
    }
}
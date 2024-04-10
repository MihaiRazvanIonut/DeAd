let isNavShown;
if (window.innerHeight > window.innerWidth) {
    isNavShown = false;
} else {
    isNavShown = true;
    document.getElementById("page-nav").setAttribute("class", "shown-nav");
}

function toggleNav() {
    if (isNavShown == true) {
        document.getElementById("page-nav").setAttribute("class", "hidden-nav");
        if (window.innerHeight > window.innerWidth) {
            document.getElementById("page-main").setAttribute("class", "shown-main");   
        }
        isNavShown = false;
    } else {
        document.getElementById("page-nav").setAttribute("class", "shown-nav");
        if (window.innerHeight > window.innerWidth) {
            document.getElementById("page-main").setAttribute("class", "hidden-main");   
        }
        isNavShown = true;
    }
}
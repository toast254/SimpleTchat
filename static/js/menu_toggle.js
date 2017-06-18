var menuToggle = document.getElementById("menu_toggle");
var menuContent = document.getElementById("menu_content");
menuToggle.addEventListener("click", function() {
    if (menuContent.classList.contains("is-active")) {
        menuContent.classList.remove("is-active");
    } else {
        menuContent.classList.add("is-active");
    }
}, false);

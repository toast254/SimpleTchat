var menu_toggle = document.getElementById("menu_toggle");
var menu_content = document.getElementById("menu_content");
menu_toggle.addEventListener("click", function(e) {
    if (menu_content.classList.contains("is-active")) {
        menu_content.classList.remove("is-active");
    } else {
        menu_content.classList.add("is-active");
    }
}, false);

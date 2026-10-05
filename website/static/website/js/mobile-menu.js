
document.addEventListener("DOMContentLoaded", function () {

    const button = document.querySelector(".mobile-menu-toggle");
    const menu = document.querySelector(".main-nav");

    if (!button || !menu) return;

    button.addEventListener("click", function () {
        menu.classList.toggle("mobile-open");
    });

    menu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            menu.classList.remove("mobile-open");
        });
    });

});


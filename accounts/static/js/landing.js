document.addEventListener("DOMContentLoaded", function () {
    const menu = document.getElementById("sideMenu");
    const openBtn = document.querySelector(".menu-btn");
    const closeBtn = document.querySelector(".close-btn");

    function toggleMenu() {
        menu.classList.toggle("open");
    }

    openBtn.addEventListener("click", toggleMenu);
    closeBtn.addEventListener("click", toggleMenu);

    document.addEventListener("click", function (event) {
        if (!menu.contains(event.target) && !openBtn.contains(event.target)) {
            menu.classList.remove("open");
        }
    });
});
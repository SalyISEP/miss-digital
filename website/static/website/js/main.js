const menuToggle = document.getElementById("menuToggle");
const mainNav = document.getElementById("mainNav");


if (menuToggle && mainNav) {

    menuToggle.addEventListener("click", () => {
        mainNav.classList.toggle("active");
    });

}


document.querySelectorAll("#mainNav a").forEach(link => {

    link.addEventListener("click", () => {

        if (mainNav) {
            mainNav.classList.remove("active");
        }

    });

});



/* ANIMATIONS */

const revealElements = document.querySelectorAll(
    ".service-card, .project-card, .founder-content, .news-card, .organization-grid div"
);


const observer = new IntersectionObserver(
    entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("visible");

                observer.unobserve(entry.target);

            }

        });

    },
    {
        threshold: 0.12
    }
);


revealElements.forEach(element => {

    element.classList.add("reveal");

    observer.observe(element);

});

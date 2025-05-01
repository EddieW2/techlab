let slideIndex = 0;
const slides = document.querySelectorAll('.slides img');

function showSlides() {
    slides.forEach((slide, index) => {
        slide.style.display = (index === slideIndex) ? 'block' : 'none';
    });
    slideIndex = (slideIndex + 1) % slides.length;
}

setInterval(showSlides, 3000);
showSlides();

document.querySelector('.menu-toggle').addEventListener('click', function () {
    document.querySelector('.sidebar').classList.toggle('show');
});

const productRows = document.querySelectorAll('.product-row');
productRows.forEach(row => {
    row.addEventListener('wheel', (e) => {
        e.preventDefault();
        row.scrollLeft += e.deltaY * 2;
    });
});

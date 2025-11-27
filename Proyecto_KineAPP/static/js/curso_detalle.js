// static/js/curso_detalle.js

document.addEventListener("DOMContentLoaded", () => {
    const sections = Array.from(document.querySelectorAll(".content-section"));
    const cards = Array.from(document.querySelectorAll(".overview__card"));
    const btnPrev = document.getElementById("btnPrev");
    const btnNext = document.getElementById("btnNext");

    if (!sections.length || !cards.length) return;

    // Orden de las secciones (coincide con data-target de las cards)
    const order = sections.map(sec => sec.dataset.section);
    let currentIndex = 0;

    function showSectionByIndex(index) {
        currentIndex = index;

        const targetName = order[currentIndex];

        sections.forEach(sec => {
            if (sec.dataset.section === targetName) {
                sec.classList.add("show");
            } else {
                sec.classList.remove("show");
            }
        });

        cards.forEach(card => {
            if (card.dataset.target === targetName) {
                card.classList.add("overview__card--active");
            } else {
                card.classList.remove("overview__card--active");
            }
        });
    }

    // Click en las tarjetas del índice
    cards.forEach((card, index) => {
        card.addEventListener("click", () => {
            showSectionByIndex(index);
        });
    });

    // Botones Anterior / Siguiente
    if (btnPrev) {
        btnPrev.addEventListener("click", () => {
            const newIndex = (currentIndex - 1 + order.length) % order.length;
            showSectionByIndex(newIndex);
        });
    }

    if (btnNext) {
        btnNext.addEventListener("click", () => {
            const newIndex = (currentIndex + 1) % order.length;
            showSectionByIndex(newIndex);
        });
    }

    // Mostrar por defecto la primera sección
    showSectionByIndex(0);
});

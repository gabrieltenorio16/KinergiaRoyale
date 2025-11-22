// ============================
// SISTEMA DE SECCIONES
// ============================

const sections = Array.from(document.querySelectorAll(".content-section"));
const overview = document.getElementById("overview");
const btnIndex = document.getElementById("btnIndex");
const btnNext = document.getElementById("btnNext");
const btnPrev = document.getElementById("btnPrev");

const order = ["presentacion", "indice", "pacientes", "contenidos"];
let currentIndex = 0;


// ----------------------------
// Mostrar una sección
// ----------------------------
function showSection(key) {
    sections.forEach(sec => {
        sec.classList.toggle("show", sec.dataset.section === key);
    });

    currentIndex = order.indexOf(key);
    updateButtons();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ----------------------------
// Actualizar botones
// ----------------------------
function updateButtons() {

    // Botón PREV
    btnPrev.disabled = currentIndex === 0;
    btnPrev.style.opacity = currentIndex === 0 ? 0.5 : 1;

    // Botón NEXT
    if (currentIndex === order.length - 1) {
        btnNext.textContent = "Volver al inicio del módulo ⬆";
    } else {
        btnNext.textContent = "Siguiente ➡";
    }
}


// ----------------------------
// Evento: abrir OVERVIEW
// ----------------------------
btnIndex.addEventListener("click", () => {
    overview.classList.add("active");
});


// ----------------------------
// Evento: clic fuera del OVERVIEW
// ----------------------------
overview.addEventListener("click", e => {
    if (e.target === overview) {
        overview.classList.remove("active");
    }
});


// ----------------------------
// Evento: seleccionar sección desde overview
// ----------------------------
document.querySelectorAll(".overview__card").forEach(card => {
    card.addEventListener("click", () => {
        const target = card.dataset.target;
        showSection(target);
        overview.classList.remove("active");
    });
});


// ----------------------------
// Botón NEXT
// ----------------------------
btnNext.addEventListener("click", () => {
    if (currentIndex < order.length - 1) {
        showSection(order[currentIndex + 1]);
    } else {
        showSection(order[0]);
    }
});


// ----------------------------
// Botón PREV
// ----------------------------
btnPrev.addEventListener("click", () => {
    if (currentIndex > 0) {
        showSection(order[currentIndex - 1]);
    }
});


// ----------------------------
// Estado inicial
// ----------------------------
showSection("presentacion");

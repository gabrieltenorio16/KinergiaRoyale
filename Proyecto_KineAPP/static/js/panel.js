// ---------- MANEJO DE MODAL ----------
const btnNotif = document.getElementById('btnNotificaciones');
const modal = document.getElementById('modalNotificaciones');
const btnCerrar = document.getElementById('btnCerrarModal');
const badge = document.getElementById('badgeCount');

const openModal = () => {
    modal.setAttribute('aria-hidden', 'false');
    if (badge) {
        badge.textContent = '0';
        badge.style.background = '#999';
    }
};

const closeModal = () => {
    modal.setAttribute('aria-hidden', 'true');
};

btnNotif.addEventListener('click', openModal);
btnCerrar.addEventListener('click', closeModal);

modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
});

document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') {
        closeModal();
    }
});


// ---------- BARRA DE PROGRESO ----------
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".progress__bar").forEach(bar => {
        const value = bar.dataset.progress;
        bar.style.width = value + "%";
    });
});

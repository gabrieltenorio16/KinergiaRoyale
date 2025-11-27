document.addEventListener("DOMContentLoaded", () => {
    // =========================================================
    //  MODAL DE NOTIFICACIONES
    // =========================================================
    const btnNotif = document.getElementById("btnNotificaciones");
    const modal = document.getElementById("modalNotificaciones");
    const btnCerrar = document.getElementById("btnCerrarModal");
    const badge = document.getElementById("badgeCount");

    const openModal = () => {
        if (!modal) return;
        modal.setAttribute("aria-hidden", "false");
        modal.classList.add("modal--open");

        if (badge) {
            badge.textContent = "0";
            badge.style.background = "#999";
        }
    };

    const closeModal = () => {
        if (!modal) return;
        modal.setAttribute("aria-hidden", "true");
        modal.classList.remove("modal--open");
    };

    if (btnNotif) {
        btnNotif.addEventListener("click", openModal);
    }

    if (btnCerrar) {
        btnCerrar.addEventListener("click", closeModal);
    }

    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) closeModal();
        });
    }

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && modal && modal.getAttribute("aria-hidden") === "false") {
            closeModal();
        }
    });

    // =========================================================
    //  BARRA DE PROGRESO
    // =========================================================
    document.querySelectorAll(".progress__bar").forEach((bar) => {
        const value = bar.dataset.progress;
        bar.style.width = value + "%";
    });

    // =========================================================
    //  MENÚ DE USUARIO (AVATAR + CERRAR SESIÓN)
    // =========================================================
    const userMenuToggle = document.getElementById("userMenuToggle");
    const userMenuDropdown = document.getElementById("userMenuDropdown");

    if (userMenuToggle && userMenuDropdown) {
        // abrir/cerrar al hacer clic en el avatar
        userMenuToggle.addEventListener("click", (e) => {
            e.stopPropagation(); // evita que se cierre al instante
            userMenuDropdown.classList.toggle("user-menu__dropdown--open");
        });

        // cerrar al hacer clic en cualquier parte del documento
        document.addEventListener("click", () => {
            userMenuDropdown.classList.remove("user-menu__dropdown--open");
        });

        // que los clics dentro del menú NO lo cierren
        userMenuDropdown.addEventListener("click", (e) => {
            e.stopPropagation();
        });
    }
});

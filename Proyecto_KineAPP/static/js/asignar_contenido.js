/* ============================================================
   ASIGNAR CONTENIDO – LÓGICA JS
   Kinergía Royale
   ============================================================ */

/* ------------------------------------------------------------
   1) EXPANDIR / COLAPSAR UNIDADES
------------------------------------------------------------ */
document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const card = btn.closest(".card");
        const subItems = card.querySelector(".sub-items");

        if (subItems) {
            const isHidden = subItems.style.display === "none" || subItems.style.display === "";
            subItems.style.display = isHidden ? "block" : "none";
            btn.classList.toggle("rotate", isHidden);
        }
    });
});

/* ------------------------------------------------------------
   2) USER MENU SUPERIOR
------------------------------------------------------------ */
const userMenu = document.getElementById("userMenu");
const userDropdown = document.getElementById("userDropdown");
const chevron = document.querySelector(".chevron");

// Abrir/cerrar menú usuario
if (userMenu) {
    userMenu.addEventListener("click", (e) => {
        e.stopPropagation();
        const visible = userDropdown.style.display === "block";
        userDropdown.style.display = visible ? "none" : "block";
        chevron.classList.toggle("open", !visible);
    });
}

// Cerrar si se hace click fuera
document.addEventListener("click", () => {
    if (userDropdown) userDropdown.style.display = "none";
    if (chevron) chevron.classList.remove("open");
});

/* ------------------------------------------------------------
   3) SELECT PERSONALIZADO (Tipos de contenido)
------------------------------------------------------------ */
const dropdownBtn = document.querySelector(".dropdown-btn");
const dropdownPanel = document.querySelector(".dropdown-panel");

if (dropdownBtn && dropdownPanel) {
    dropdownBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const visible = dropdownPanel.style.display === "block";
        dropdownPanel.style.display = visible ? "none" : "block";
    });

    // Cerrar panel si se hace click fuera
    document.addEventListener("click", () => {
        dropdownPanel.style.display = "none";
    });

    // Evitar cierre al hacer click dentro del panel
    dropdownPanel.addEventListener("click", (e) => {
        e.stopPropagation();
    });
}

/* ------------------------------------------------------------
   4) ACCIONES: SELECCIONAR TODOS / LIMPIAR SELECCIÓN
------------------------------------------------------------ */
const filterOptions = document.querySelectorAll(".filter-option");
const selectAllBtn = document.querySelector(".select-all");
const clearSelectionBtn = document.querySelector(".clear-selection");

function updateFilterLabel() {
    const checked = Array.from(filterOptions).filter(opt => opt.checked).length;

    if (checked === 0) {
        dropdownBtn.innerText = "Todos los tipos de contenido ▾";
    } else {
        dropdownBtn.innerText = `${checked} tipos seleccionados ▾`;
    }
}

if (selectAllBtn) {
    selectAllBtn.addEventListener("click", () => {
        filterOptions.forEach(opt => opt.checked = true);
        updateFilterLabel();
    });
}

if (clearSelectionBtn) {
    clearSelectionBtn.addEventListener("click", () => {
        filterOptions.forEach(opt => opt.checked = false);
        updateFilterLabel();
    });
}

// Actualizar texto cuando el usuario marca/desmarca cualquier checkbox
filterOptions.forEach(opt => {
    opt.addEventListener("change", updateFilterLabel);
});

/* ------------------------------------------------------------
   5) OTROS AJUSTES
------------------------------------------------------------ */
// Si necesitas más lógicas, las agregamos aquí modularmente.

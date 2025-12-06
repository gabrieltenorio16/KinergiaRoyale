/* ============================================================
   ASIGNAR PACIENTES - LÓGICA JS
   Pantalla de gestión de pacientes del curso
   ============================================================ */

/* ------------------------------------------------------------
   USER MENU SUPERIOR
------------------------------------------------------------ */
const userMenuPac = document.getElementById("userMenu");
const userDropdownPac = document.getElementById("userDropdown");
const chevronPac = document.querySelector(".chevron");

if (userMenuPac) {
    userMenuPac.addEventListener("click", (e) => {
        e.stopPropagation();
        const visible = userDropdownPac.style.display === "block";
        userDropdownPac.style.display = visible ? "none" : "block";
        chevronPac.classList.toggle("open", !visible);
    });
}

document.addEventListener("click", () => {
    if (userDropdownPac) userDropdownPac.style.display = "none";
    if (chevronPac) chevronPac.classList.remove("open");
});

/* ------------------------------------------------------------
   TABS: mostrar secciones de pacientes
------------------------------------------------------------ */
const tabsPacientes = document.querySelectorAll("#contentTabs .nav-link");
const sectionsPacientes = {
    casos: document.getElementById("section-casos"),
    diagnosticos: document.getElementById("section-diagnosticos"),
    etapas: document.getElementById("section-etapas"),
    pacientes: document.getElementById("section-pacientes"),
    partes: document.getElementById("section-partes"),
};

tabsPacientes.forEach(tab => {
    tab.addEventListener("click", (e) => {
        const target = tab.dataset.section;
        if (!target) return;
        e.preventDefault();

        tabsPacientes.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");

        Object.values(sectionsPacientes).forEach(sec => {
            if (sec) sec.classList.add("d-none");
        });

        const sec = sectionsPacientes[target];
        if (sec) sec.classList.remove("d-none");
    });
});

/* ------------------------------------------------------------
   BUSCADORES POR TABLA (filtro simple en cliente)
------------------------------------------------------------ */
const searchInputs = document.querySelectorAll("[data-table-search]");

searchInputs.forEach(input => {
    const tableId = input.dataset.tableSearch;
    const table = document.getElementById(tableId);
    if (!table) return;

    const tbody = table.querySelector("tbody");
    if (!tbody) return;

    input.addEventListener("input", () => {
        const term = input.value.trim().toLowerCase();
        const rows = tbody.querySelectorAll("tr");

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(term) ? "" : "none";
        });
    });
});

/* ------------------------------------------------------------
   MODAL CASO CLÍNICO: crear / editar
------------------------------------------------------------ */
const modalCasoEl = document.getElementById("modalCasoClinico");
let modalCaso = null;

if (modalCasoEl && window.bootstrap) {
    modalCaso = new bootstrap.Modal(modalCasoEl);
}

const formCaso = modalCasoEl ? modalCasoEl.querySelector("form") : null;
const inputAccionCaso = document.getElementById("accionCasoClinico");
const inputCasoId = document.getElementById("casoClinicoIdInput");

// Editar caso
document.querySelectorAll(".btn-editar-caso").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formCaso || !modalCaso) return;

        const id = btn.dataset.id;
        const titulo = btn.dataset.titulo || "";
        const descripcion = btn.dataset.descripcion || "";
        const pacienteId = btn.dataset.pacienteId || "";

        formCaso.reset();
        formCaso.elements["titulo"].value = titulo;
        formCaso.elements["descripcion"].value = descripcion;
        formCaso.elements["paciente"].value = pacienteId;

        if (inputAccionCaso) inputAccionCaso.value = "editar";
        if (inputCasoId) inputCasoId.value = id;

        const titleEl = modalCasoEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar caso clínico";

        modalCaso.show();
    });
});

// Crear caso (botón Añadir)
const btnAddCaso = document.getElementById("btnAddCasoClinico");
if (btnAddCaso && formCaso && modalCaso && inputAccionCaso && inputCasoId) {
    btnAddCaso.addEventListener("click", () => {
        formCaso.reset();
        inputAccionCaso.value = "crear";
        inputCasoId.value = "";
        const titleEl = modalCasoEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nuevo caso clínico";
    });
}

/* ------------------------------------------------------------
   MODAL PACIENTE: crear / editar
------------------------------------------------------------ */
const modalPacienteEl = document.getElementById("modalPaciente");
let modalPaciente = null;

if (modalPacienteEl && window.bootstrap) {
    modalPaciente = new bootstrap.Modal(modalPacienteEl);
}

const formPaciente = modalPacienteEl ? modalPacienteEl.querySelector("form") : null;
const inputAccionPaciente = document.getElementById("accionPaciente");
const inputPacienteId = document.getElementById("pacienteIdInput");

// Editar paciente
document.querySelectorAll(".btn-editar-paciente").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formPaciente || !modalPaciente) return;

        const id = btn.dataset.id;
        const nombres = btn.dataset.nombres || "";
        const apellidos = btn.dataset.apellidos || "";
        const edad = btn.dataset.edad || "";
        const antecedentes = btn.dataset.antecedentes || "";
        const historial = btn.dataset.historial || "";

        formPaciente.reset();

        formPaciente.elements["nombres"].value = nombres;
        formPaciente.elements["apellidos"].value = apellidos;
        formPaciente.elements["edad"].value = edad;
        formPaciente.elements["antecedentes"].value = antecedentes;
        formPaciente.elements["historial_medico"].value = historial;

        if (inputAccionPaciente) inputAccionPaciente.value = "editar";
        if (inputPacienteId) inputPacienteId.value = id;

        const titleEl = modalPacienteEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar paciente";

        modalPaciente.show();
    });
});

// Crear paciente
const btnAddPaciente = document.getElementById("btnAddPaciente");
if (btnAddPaciente && formPaciente && modalPaciente && inputAccionPaciente && inputPacienteId) {
    btnAddPaciente.addEventListener("click", () => {
        formPaciente.reset();
        inputAccionPaciente.value = "crear";
        inputPacienteId.value = "";
        const titleEl = modalPacienteEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nuevo paciente";
    });
}


/* ------------------------------------------------------------
   CHECKBOXES + BORRADO MÚLTIPLE (todas las tablas)
------------------------------------------------------------ */
function setupBulkDelete(masterId, itemClass, buttonId, emptyMsg, confirmMsg) {
    const master = document.getElementById(masterId);
    const button = document.getElementById(buttonId);

    if (master) {
        master.addEventListener("change", (e) => {
            const checked = e.target.checked;
            document.querySelectorAll("." + itemClass).forEach(chk => {
                chk.checked = checked;
            });
        });
    }

    if (button) {
        button.addEventListener("click", (e) => {
            const seleccionados = document.querySelectorAll("." + itemClass + ":checked").length;
            if (!seleccionados) {
                alert(emptyMsg);
                e.preventDefault();
                return;
            }
            const ok = confirm(confirmMsg);
            if (!ok) {
                e.preventDefault();
            }
        });
    }
}

/* ------------------------------------------------------------
   MODAL DIAGNÓSTICO: crear / editar
------------------------------------------------------------ */
const modalDiagEl = document.getElementById("modalDiagnostico");
let modalDiag = null;

if (modalDiagEl && window.bootstrap) {
    modalDiag = new bootstrap.Modal(modalDiagEl);
}

const formDiag = modalDiagEl ? modalDiagEl.querySelector("form") : null;
const inputAccionDiag = document.getElementById("accionDiagnostico");
const inputDiagId = document.getElementById("diagnosticoIdInput");
const pacienteSelectDiag = formDiag ? formDiag.elements["paciente"] : null;
const casoSelectDiag = formDiag ? formDiag.elements["caso"] : null;

const filterCasosPorPaciente = (preserveSelection) => {
    if (!casoSelectDiag) return;
    const pacienteId = pacienteSelectDiag ? pacienteSelectDiag.value : "";
    const previousValue = preserveSelection ? casoSelectDiag.value : "";
    let firstVisibleValue = "";

    Array.from(casoSelectDiag.options).forEach(opt => {
        if (!opt.value) {
            opt.hidden = false;
            opt.disabled = false;
            return;
        }
        const matchesPaciente = !pacienteId || opt.dataset.pacienteId === pacienteId;
        opt.hidden = !matchesPaciente;
        opt.disabled = !matchesPaciente;
        if (matchesPaciente && !firstVisibleValue) {
            firstVisibleValue = opt.value;
        }
    });

    if (preserveSelection && previousValue) {
        const prevOption = Array.from(casoSelectDiag.options).find(
            opt => opt.value === previousValue && !opt.disabled
        );
        if (prevOption) {
            casoSelectDiag.value = previousValue;
            return;
        }
    }

    if (pacienteId) {
        if (preserveSelection) {
            casoSelectDiag.value = firstVisibleValue || "";
        } else {
            casoSelectDiag.value = "";
        }
    } else {
        casoSelectDiag.value = "";
    }
};

if (pacienteSelectDiag) {
    pacienteSelectDiag.addEventListener("change", () => filterCasosPorPaciente(false));
}

filterCasosPorPaciente(true);

// Editar diagnóstico
document.querySelectorAll(".btn-editar-diagnostico").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formDiag || !modalDiag) return;

        const id = btn.dataset.id;
        const pacienteId = btn.dataset.pacienteId || "";
        const casoId = btn.dataset.casoId || "";
        const descripcion = btn.dataset.descripcion || "";

        formDiag.reset();

        if (pacienteSelectDiag) pacienteSelectDiag.value = pacienteId;
        if (casoSelectDiag) casoSelectDiag.value = casoId;
        formDiag.elements["descripcion"].value = descripcion;
        filterCasosPorPaciente(true);

        if (inputAccionDiag) inputAccionDiag.value = "editar";
        if (inputDiagId) inputDiagId.value = id;

        const titleEl = modalDiagEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar diagnóstico";

        modalDiag.show();
    });
});

// Crear diagnóstico (botón Añadir)
const btnAddDiag = document.getElementById("btnAddDiagnostico");
if (btnAddDiag && formDiag && modalDiag && inputAccionDiag && inputDiagId) {
    btnAddDiag.addEventListener("click", () => {
        formDiag.reset();
        inputAccionDiag.value = "crear";
        inputDiagId.value = "";
        filterCasosPorPaciente(false);
        const titleEl = modalDiagEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nuevo diagnóstico";
    });
}


// Casos clínicos
setupBulkDelete(
    "chkTodosCasos",
    "chk-caso",
    "btnBorrarCasos",
    "Selecciona al menos un caso clínico para borrar.",
    "¿Estás seguro de borrar los casos seleccionados? Esta acción no se puede deshacer."
);

// Pacientes
setupBulkDelete(
    "chkTodosPacientes",
    "chk-paciente",
    "btnBorrarPacientes",
    "Selecciona al menos un paciente para borrar.",
    "¿Estás seguro de borrar los pacientes seleccionados? Esta acción no se puede deshacer."
);

setupBulkDelete(
    "chkTodosDiagnosticos",
    "chk-diagnostico",
    "btnBorrarDiagnosticos",
    "Selecciona al menos un diagnóstico para borrar.",
    "¿Estás seguro de borrar los diagnósticos seleccionados? Esta acción no se puede deshacer."
);

// (cuando agregues los formularios de borrado para Diagnósticos, Etapas y Partes del cuerpo,
// solo tendrás que llamar a setupBulkDelete con sus IDs/clases)

// static/js/panel_maestro_docente.js

document.addEventListener("DOMContentLoaded", function () {
    // ============================
    // 1. Dropdown usuario
    // ============================
    const toggleBtn = document.getElementById("userMenuToggle");
    const dropdown = document.getElementById("userDropdown");

    if (toggleBtn && dropdown) {
        // Abrir / cerrar al hacer click en el usuario
        toggleBtn.addEventListener("click", function (e) {
            e.stopPropagation(); // evita que el click burbujee y lo cierre inmediatamente
            dropdown.classList.toggle("show");
        });

        // Cerrar al hacer click fuera
        document.addEventListener("click", function (e) {
            if (!dropdown.contains(e.target) && !toggleBtn.contains(e.target)) {
                dropdown.classList.remove("show");
            }
        });
    }

    // ============================
    // 2. Buscador de cursos (panel Clases)
    // ============================
    const buscadorCursos = document.getElementById("buscadorCursos");
    const courseCards = document.querySelectorAll(".course-card");

    if (buscadorCursos && courseCards.length > 0) {
        buscadorCursos.addEventListener("input", function () {
            const term = this.value.trim().toLowerCase();

            courseCards.forEach(card => {
                const nombre = card.dataset.cursoNombre || "";
                const textoCompleto = card.textContent.toLowerCase();

                const coincide = nombre.includes(term) || textoCompleto.includes(term);
                card.style.display = coincide ? "" : "none";
            });
        });
    }

    // ============================
    // 3. Modal "Agregar estudiantes"
    // ============================
    const modalAgregarEstudiantes = document.getElementById("modalAgregarEstudiantes");
    const formAgregarEstudiantes = document.getElementById("formAgregarEstudiantes");
    const nombreCursoSpan = document.getElementById("nombreCursoSeleccionado");
    const chkTodosEstudiantes = document.getElementById("chkTodosEstudiantes");
    const buscadorEstudiantes = document.getElementById("buscadorEstudiantes");
    const btnAgregarEstudiantes = document.getElementById("btnAgregarEstudiantes");
    const btnQuitarEstudiantes = document.getElementById("btnQuitarEstudiantes");
    const accionEstudiantes = document.getElementById("accionEstudiantes");

    // Abrir modal con contexto del curso
    const botonesAgregar = document.querySelectorAll(".btn-agregar-estudiantes");

    if (modalAgregarEstudiantes && formAgregarEstudiantes) {
        botonesAgregar.forEach(btn => {
            btn.addEventListener("click", function () {
                const cursoId = this.dataset.cursoId;
                const cursoNombre = this.dataset.cursoNombre || "";

                // Configurar título del modal
                if (nombreCursoSpan) {
                    nombreCursoSpan.textContent = `“${cursoNombre}”`;
                }

                // Configurar action del formulario para este curso
                formAgregarEstudiantes.action = `/docente/curso/${cursoId}/agregar-estudiantes/`;

                // Reset de selección
                const checks = formAgregarEstudiantes.querySelectorAll(".chk-estudiante");
                checks.forEach(chk => { chk.checked = false; });
                if (chkTodosEstudiantes) chkTodosEstudiantes.checked = false;

                // Acción por defecto: agregar
                if (accionEstudiantes) accionEstudiantes.value = "agregar";

                // Abrir modal vía Bootstrap
                const modal = new bootstrap.Modal(modalAgregarEstudiantes);
                modal.show();
            });
        });

        // Seleccionar / deseleccionar todos
        if (chkTodosEstudiantes) {
            chkTodosEstudiantes.addEventListener("change", function () {
                const checks = formAgregarEstudiantes.querySelectorAll(".chk-estudiante");
                checks.forEach(chk => {
                    chk.checked = chkTodosEstudiantes.checked;
                });
            });
        }

        // Filtro en tabla de estudiantes
        if (buscadorEstudiantes) {
            buscadorEstudiantes.addEventListener("input", function () {
                const term = this.value.trim().toLowerCase();
                const filas = formAgregarEstudiantes.querySelectorAll("#tablaEstudiantes tr");

                filas.forEach(tr => {
                    const texto = tr.textContent.toLowerCase();
                    tr.style.display = texto.includes(term) ? "" : "none";
                });
            });
        }

        // Botón "Agregar seleccionados"
        if (btnAgregarEstudiantes && accionEstudiantes) {
            btnAgregarEstudiantes.addEventListener("click", function () {
                accionEstudiantes.value = "agregar";
                formAgregarEstudiantes.submit();
            });
        }

        // Botón "Quitar seleccionados"
        if (btnQuitarEstudiantes && accionEstudiantes) {
            btnQuitarEstudiantes.addEventListener("click", function () {
                accionEstudiantes.value = "quitar";
                formAgregarEstudiantes.submit();
            });
        }
    }

    // ============================
    // 4. Buscador global en pestaña Estudiantes
    // ============================
    const buscadorEstudiantesGlobal = document.getElementById("buscadorEstudiantesGlobal");
    const tablaEstudiantesGlobal = document.getElementById("tablaEstudiantesGlobal");

    if (buscadorEstudiantesGlobal && tablaEstudiantesGlobal) {
        buscadorEstudiantesGlobal.addEventListener("input", function () {
            const term = this.value.trim().toLowerCase();
            const filas = tablaEstudiantesGlobal.querySelectorAll("tbody tr");

            filas.forEach(tr => {
                const texto = tr.textContent.toLowerCase();
                tr.style.display = texto.includes(term) ? "" : "none";
            });
        });
    }

    // ============================
    // 5. Placeholder Importar Excel/CSV
    // ============================
    const btnImportarExcel = document.getElementById("btnImportarExcel");
    if (btnImportarExcel) {
        btnImportarExcel.addEventListener("click", function () {
            alert("Importación desde Excel/CSV quedará para una siguiente iteración. La UI ya está preparada.");
        });
    }

});


// ============================
// 6. Click en zona click (abrir asignar contenido)
// ============================
document.querySelectorAll(".zone-click").forEach(zone => {
    zone.addEventListener("click", function () {
        const url = this.dataset.url;
        if (url) {
            window.location.href = url;
        }
    });
});





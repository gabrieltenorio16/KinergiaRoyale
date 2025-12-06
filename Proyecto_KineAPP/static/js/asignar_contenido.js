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
   6) BORRAR TEMAS: confirmación y seleccionar todos
------------------------------------------------------------ */
const chkTodosTemas = document.getElementById("chkTodosTemas");
const btnBorrarTemas = document.getElementById("btnBorrarTemas");

if (chkTodosTemas) {
    chkTodosTemas.addEventListener("change", (e) => {
        const checked = e.target.checked;
        document.querySelectorAll(".chk-tema").forEach(chk => {
            chk.checked = checked;
        });
    });
}

if (btnBorrarTemas) {
    btnBorrarTemas.addEventListener("click", (e) => {
        const seleccionados = document.querySelectorAll(".chk-tema:checked").length;
        if (!seleccionados) {
            alert("Selecciona al menos un tema para borrar.");
            e.preventDefault();
            return;
        }
        const ok = confirm(
            "¿Estás seguro de borrar los temas seleccionados? Esta acción no se puede deshacer."
        );
        if (!ok) {
            e.preventDefault();
        }
    });
}

/* ------------------------------------------------------------
   7) EDITAR TEMA: abrir modal con datos
------------------------------------------------------------ */
const modalCrearTemaEl = document.getElementById("modalCrearTema");
let modalCrearTema = null;

if (modalCrearTemaEl && window.bootstrap) {
    modalCrearTema = new bootstrap.Modal(modalCrearTemaEl);
}

const formTema = modalCrearTemaEl ? modalCrearTemaEl.querySelector("form") : null;
const inputAccion = document.getElementById("accionTema");
const inputTemaId = document.getElementById("temaIdInput");

document.querySelectorAll(".btn-editar-tema").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formTema || !modalCrearTema) return;

        const id = btn.dataset.id;
        const titulo = btn.dataset.titulo || "";
        const descripcion = btn.dataset.descripcion || "";
        const estado = btn.dataset.estado === "1";
        const fechaInicio = btn.dataset.fechaInicio || "";
        const fechaFin = btn.dataset.fechaFin || "";

        formTema.reset();

        formTema.elements["titulo"].value = titulo;
        formTema.elements["descripcion"].value = descripcion;
        formTema.elements["estado_completado"].checked = estado;
        formTema.elements["fecha_inicio"].value = fechaInicio;
        formTema.elements["fecha_fin"].value = fechaFin;

        if (inputAccion) inputAccion.value = "editar";
        if (inputTemaId) inputTemaId.value = id;

        const titleEl = modalCrearTemaEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar tema";

        modalCrearTema.show();
    });
});

// Resetear modal cuando se crea un tema nuevo
const btnAddTema = document.getElementById("btnAddTema");
if (btnAddTema && formTema && modalCrearTema && inputAccion && inputTemaId) {
    btnAddTema.addEventListener("click", () => {
        formTema.reset();
        inputAccion.value = "crear";
        inputTemaId.value = "";
        const titleEl = modalCrearTemaEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nuevo tema";
    });
}

/* ------------------------------------------------------------
   8) BUSCADOR DE TEMAS (por título / descripción)
------------------------------------------------------------ */
const buscadorTemas = document.getElementById("buscadorTemas");

if (buscadorTemas) {
    buscadorTemas.addEventListener("input", () => {
        const termino = buscadorTemas.value.trim().toLowerCase();
        const filas = document.querySelectorAll(".unit-list-container table tbody tr");

        filas.forEach(fila => {
            const esFilaVacia = fila.dataset.empty === "1";

            if (esFilaVacia) {
                // solo mostramos la fila "no hay temas" cuando no hay término de búsqueda
                fila.style.display = termino ? "none" : "";
                return;
            }

            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(termino) ? "" : "none";
        });
    });
}

/* ------------------------------------------------------------
   12) TABS: mostrar Temas / Videos
------------------------------------------------------------ */
const tabsContenido = document.querySelectorAll("#contentTabs .nav-link");
const sectionsModulo = {
    temas: document.getElementById("section-temas"),
    videos: document.getElementById("section-videos"),
    topicos: document.getElementById("section-topicos"),
    preguntas: document.getElementById("section-preguntas"),
    respuestas: document.getElementById("section-respuestas"),
};

tabsContenido.forEach(tab => {
    tab.addEventListener("click", (e) => {
        const target = tab.dataset.section;
        if (!target) {
            // Tabs sin sección (tópicos, preguntas, etc.) aún no hacen nada
            return;
        }
        e.preventDefault();

        // Marcar tab activa
        tabsContenido.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");

        // Ocultar todas las secciones conocidas
        Object.values(sectionsModulo).forEach(sec => {
            if (sec) sec.classList.add("d-none");
        });

        // Mostrar la sección seleccionada
        const sec = sectionsModulo[target];
        if (sec) sec.classList.remove("d-none");
    });
});


/* ------------------------------------------------------------
   9) BORRAR VIDEOS: confirmación y seleccionar todos
------------------------------------------------------------ */
const chkTodosVideos = document.getElementById("chkTodosVideos");
const btnBorrarVideos = document.getElementById("btnBorrarVideos");

if (chkTodosVideos) {
    chkTodosVideos.addEventListener("change", (e) => {
        const checked = e.target.checked;
        document.querySelectorAll(".chk-video").forEach(chk => {
            chk.checked = checked;
        });
    });
}

if (btnBorrarVideos) {
    btnBorrarVideos.addEventListener("click", (e) => {
        const seleccionados = document.querySelectorAll(".chk-video:checked").length;
        if (!seleccionados) {
            alert("Selecciona al menos un video para borrar.");
            e.preventDefault();
            return;
        }
        const ok = confirm(
            "¿Estás seguro de borrar los videos seleccionados? Esta acción no se puede deshacer."
        );
        if (!ok) {
            e.preventDefault();
        }
    });
}

/* ------------------------------------------------------------
   10) EDITAR VIDEO: abrir modal con datos
------------------------------------------------------------ */
const modalCrearVideoEl = document.getElementById("modalCrearVideo");
let modalCrearVideo = null;

if (modalCrearVideoEl && window.bootstrap) {
    modalCrearVideo = new bootstrap.Modal(modalCrearVideoEl);
}

const formVideo = modalCrearVideoEl ? modalCrearVideoEl.querySelector("form") : null;
const inputAccionVideo = document.getElementById("accionVideo");
const inputVideoId = document.getElementById("videoIdInput");

document.querySelectorAll(".btn-editar-video").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formVideo || !modalCrearVideo) return;

        const id = btn.dataset.id;
        const titulo = btn.dataset.titulo || "";
        const url = btn.dataset.url || "";
        const temaId = btn.dataset.temaId || "";

        formVideo.reset();

        formVideo.elements["titulo"].value = titulo;
        formVideo.elements["url"].value = url;
        formVideo.elements["tema"].value = temaId;

        inputAccionVideo.value = "editar";
        inputVideoId.value = id;

        const titleEl = modalCrearVideoEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar video";

        modalCrearVideo.show();
    });
});

// Resetear modal cuando se crea un video nuevo
const btnAddVideo = document.getElementById("btnAddVideo");
if (btnAddVideo && formVideo && modalCrearVideo && inputAccionVideo && inputVideoId) {
    btnAddVideo.addEventListener("click", () => {
        formVideo.reset();
        inputAccionVideo.value = "crear";
        inputVideoId.value = "";
        const titleEl = modalCrearVideoEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nuevo video";
    });
}

/* ------------------------------------------------------------
   11) BUSCADOR DE VIDEOS
------------------------------------------------------------ */
const buscadorVideos = document.getElementById("buscadorVideos");

if (buscadorVideos) {
    buscadorVideos.addEventListener("input", () => {
        const termino = buscadorVideos.value.trim().toLowerCase();
        const filas = document.querySelectorAll("#tablaVideos tbody tr");

        filas.forEach(fila => {
            const esFilaVacia = fila.dataset.emptyVideos === "1";
            if (esFilaVacia) {
                fila.style.display = termino ? "none" : "";
                return;
            }

            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(termino) ? "" : "none";
        });
    });
}

/* ------------------------------------------------------------
   13) BORRAR TÓPICOS: confirmación y seleccionar todos
------------------------------------------------------------ */
const chkTodosTopicos = document.getElementById("chkTodosTopicos");
const btnBorrarTopicos = document.getElementById("btnBorrarTopicos");

if (chkTodosTopicos) {
    chkTodosTopicos.addEventListener("change", (e) => {
        const checked = e.target.checked;
        document.querySelectorAll(".chk-topico").forEach(chk => {
            chk.checked = checked;
        });
    });
}

if (btnBorrarTopicos) {
    btnBorrarTopicos.addEventListener("click", (e) => {
        const seleccionados = document.querySelectorAll(".chk-topico:checked").length;
        if (!seleccionados) {
            alert("Selecciona al menos un tópico para borrar.");
            e.preventDefault();
            return;
        }
        const ok = confirm(
            "¿Estás seguro de borrar los tópicos seleccionados? Esta acción no se puede deshacer."
        );
        if (!ok) {
            e.preventDefault();
        }
    });
}

/* ------------------------------------------------------------
   14) EDITAR TÓPICO: abrir modal con datos
------------------------------------------------------------ */
const modalCrearTopicoEl = document.getElementById("modalCrearTopico");
let modalCrearTopico = null;

if (modalCrearTopicoEl && window.bootstrap) {
    modalCrearTopico = new bootstrap.Modal(modalCrearTopicoEl);
}

const formTopico = modalCrearTopicoEl ? modalCrearTopicoEl.querySelector("form") : null;
const inputAccionTopico = document.getElementById("accionTopico");
const inputTopicoId = document.getElementById("topicoIdInput");

document.querySelectorAll(".btn-editar-topico").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formTopico || !modalCrearTopico) return;

        const id = btn.dataset.id;
        const nombre = btn.dataset.nombre || "";
        const descripcion = btn.dataset.descripcion || "";

        formTopico.reset();

        formTopico.elements["nombre"].value = nombre;
        formTopico.elements["descripcion"].value = descripcion;

        inputAccionTopico.value = "editar";
        inputTopicoId.value = id;

        const titleEl = modalCrearTopicoEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar tópico";

        modalCrearTopico.show();
    });
});

// Resetear modal cuando se crea un tópico nuevo
const btnAddTopico = document.getElementById("btnAddTopico");
if (btnAddTopico && formTopico && modalCrearTopico && inputAccionTopico && inputTopicoId) {
    btnAddTopico.addEventListener("click", () => {
        formTopico.reset();
        inputAccionTopico.value = "crear";
        inputTopicoId.value = "";
        const titleEl = modalCrearTopicoEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nuevo tópico";
    });
}

/* ------------------------------------------------------------
   15) BUSCADOR DE TÓPICOS
------------------------------------------------------------ */
const buscadorTopicos = document.getElementById("buscadorTopicos");

if (buscadorTopicos) {
    buscadorTopicos.addEventListener("input", () => {
        const termino = buscadorTopicos.value.trim().toLowerCase();
        const filas = document.querySelectorAll("#tablaTopicos tbody tr");

        filas.forEach(fila => {
            const esFilaVacia = fila.dataset.emptyTopicos === "1";
            if (esFilaVacia) {
                fila.style.display = termino ? "none" : "";
                return;
            }

            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(termino) ? "" : "none";
        });
    });
}
/* ------------------------------------------------------------
   16) VER TÓPICO: mostrar preguntas en modal
------------------------------------------------------------ */
const modalVerTopicoEl = document.getElementById("modalVerTopico");
let modalVerTopico = null;

if (modalVerTopicoEl && window.bootstrap) {
    modalVerTopico = new bootstrap.Modal(modalVerTopicoEl);
}

const verTopicoNombre = document.getElementById("verTopicoNombre");
const verTopicoDescripcion = document.getElementById("verTopicoDescripcion");
const verTopicoPreguntas = document.getElementById("verTopicoPreguntas");

document.querySelectorAll(".btn-ver-topico").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!modalVerTopico) return;

        const id = btn.dataset.id;
        const nombre = btn.dataset.nombre || "";
        const descripcion = btn.dataset.descripcion || "";

        const contenedorPreguntas = document.getElementById(`preguntas-topico-${id}`);

        if (verTopicoNombre) verTopicoNombre.textContent = nombre;
        if (verTopicoDescripcion) {
            verTopicoDescripcion.textContent = descripcion || "Sin descripción.";
        }

        if (verTopicoPreguntas) {
            if (contenedorPreguntas) {
                // Reusar el HTML ya renderizado en el div oculto
                verTopicoPreguntas.innerHTML = contenedorPreguntas.innerHTML;
            } else {
                verTopicoPreguntas.innerHTML =
                    "<p class='text-muted mb-0'>No se encontraron preguntas para este tópico.</p>";
            }
        }

        modalVerTopico.show();
    });
});

/* ------------------------------------------------------------
   17) BORRAR PREGUNTAS: confirmación y seleccionar todos
------------------------------------------------------------ */
const chkTodosPreguntas = document.getElementById("chkTodosPreguntas");
const btnBorrarPreguntas = document.getElementById("btnBorrarPreguntas");

if (chkTodosPreguntas) {
    chkTodosPreguntas.addEventListener("change", (e) => {
        const checked = e.target.checked;
        document.querySelectorAll(".chk-pregunta").forEach(chk => {
            chk.checked = checked;
        });
    });
}

if (btnBorrarPreguntas) {
    btnBorrarPreguntas.addEventListener("click", (e) => {
        const seleccionados = document.querySelectorAll(".chk-pregunta:checked").length;
        if (!seleccionados) {
            alert("Selecciona al menos una pregunta para borrar.");
            e.preventDefault();
            return;
        }
        const ok = confirm(
            "¿Estás seguro de borrar las preguntas seleccionadas? Esta acción no se puede deshacer."
        );
        if (!ok) {
            e.preventDefault();
        }
    });
}

/* ------------------------------------------------------------
   18) EDITAR PREGUNTA: abrir modal con datos
------------------------------------------------------------ */
const modalCrearPreguntaEl = document.getElementById("modalCrearPregunta");
let modalCrearPregunta = null;

if (modalCrearPreguntaEl && window.bootstrap) {
    modalCrearPregunta = new bootstrap.Modal(modalCrearPreguntaEl);
}

const formPregunta = modalCrearPreguntaEl ? modalCrearPreguntaEl.querySelector("form") : null;
const inputAccionPregunta = document.getElementById("accionPregunta");
const inputPreguntaId = document.getElementById("preguntaIdInput");

document.querySelectorAll(".btn-editar-pregunta").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formPregunta || !modalCrearPregunta) return;

        const id = btn.dataset.id;
        const texto = btn.dataset.texto || "";
        const topicoId = btn.dataset.topicoId || "";

        formPregunta.reset();

        formPregunta.elements["pregunta"].value = texto;
        formPregunta.elements["topico"].value = topicoId;

        inputAccionPregunta.value = "editar";
        inputPreguntaId.value = id;

        const titleEl = modalCrearPreguntaEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar pregunta";

        modalCrearPregunta.show();
    });
});

// Resetear modal cuando se crea una pregunta nueva
const btnAddPregunta = document.getElementById("btnAddPregunta");
if (btnAddPregunta && formPregunta && modalCrearPregunta &&
    inputAccionPregunta && inputPreguntaId) {
    btnAddPregunta.addEventListener("click", () => {
        formPregunta.reset();
        inputAccionPregunta.value = "crear";
        inputPreguntaId.value = "";
        const titleEl = modalCrearPreguntaEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nueva pregunta";
    });
}

/* ------------------------------------------------------------
   19) BUSCADOR DE PREGUNTAS
------------------------------------------------------------ */
const buscadorPreguntas = document.getElementById("buscadorPreguntas");

if (buscadorPreguntas) {
    buscadorPreguntas.addEventListener("input", () => {
        const termino = buscadorPreguntas.value.trim().toLowerCase();
        const filas = document.querySelectorAll("#tablaPreguntas tbody tr");

        filas.forEach(fila => {
            const esFilaVacia = fila.dataset.emptyPreguntas === "1";
            if (esFilaVacia) {
                fila.style.display = termino ? "none" : "";
                return;
            }

            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(termino) ? "" : "none";
        });
    });
}
/* ------------------------------------------------------------
   20) BORRAR RESPUESTAS
------------------------------------------------------------ */
const chkTodosRespuestas = document.getElementById("chkTodosRespuestas");
const btnBorrarRespuestas = document.getElementById("btnBorrarRespuestas");

if (chkTodosRespuestas) {
    chkTodosRespuestas.addEventListener("change", (e) => {
        const checked = e.target.checked;
        document.querySelectorAll(".chk-respuesta").forEach(chk => {
            chk.checked = checked;
        });
    });
}

if (btnBorrarRespuestas) {
    btnBorrarRespuestas.addEventListener("click", (e) => {
        const seleccionados = document.querySelectorAll(".chk-respuesta:checked").length;
        if (!seleccionados) {
            alert("Selecciona al menos una respuesta para borrar.");
            e.preventDefault();
            return;
        }
        const ok = confirm(
            "¿Estás seguro de borrar las respuestas seleccionadas? Esta acción no se puede deshacer."
        );
        if (!ok) {
            e.preventDefault();
        }
    });
}

/* ------------------------------------------------------------
   21) EDITAR RESPUESTA
------------------------------------------------------------ */
const modalCrearRespuestaEl = document.getElementById("modalCrearRespuesta");
let modalCrearRespuesta = null;

if (modalCrearRespuestaEl && window.bootstrap) {
    modalCrearRespuesta = new bootstrap.Modal(modalCrearRespuestaEl);
}

const formRespuesta = modalCrearRespuestaEl ? modalCrearRespuestaEl.querySelector("form") : null;
const inputAccionRespuesta = document.getElementById("accionRespuesta");
const inputRespuestaId = document.getElementById("respuestaIdInput");

document.querySelectorAll(".btn-editar-respuesta").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!formRespuesta || !modalCrearRespuesta) return;

        const id = btn.dataset.id;
        const contenido = btn.dataset.contenido || "";
        const retro = btn.dataset.retro || "";
        const correcta = btn.dataset.correcta === "1";
        const preguntaId = btn.dataset.preguntaId || "";

        formRespuesta.reset();

        formRespuesta.elements["contenido"].value = contenido;
        formRespuesta.elements["retroalimentacion"].value = retro;
        formRespuesta.elements["es_correcta"].checked = correcta;
        formRespuesta.elements["pregunta"].value = preguntaId;

        inputAccionRespuesta.value = "editar";
        inputRespuestaId.value = id;

        const titleEl = modalCrearRespuestaEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Editar respuesta";

        modalCrearRespuesta.show();
    });
});

// Resetear modal cuando se crea una respuesta nueva
const btnAddRespuesta = document.getElementById("btnAddRespuesta");
if (btnAddRespuesta && formRespuesta && modalCrearRespuesta &&
    inputAccionRespuesta && inputRespuestaId) {
    btnAddRespuesta.addEventListener("click", () => {
        formRespuesta.reset();
        inputAccionRespuesta.value = "crear";
        inputRespuestaId.value = "";
        const titleEl = modalCrearRespuestaEl.querySelector(".modal-title");
        if (titleEl) titleEl.textContent = "Crear nueva respuesta";
    });
}

/* ------------------------------------------------------------
   22) BUSCADOR DE RESPUESTAS
------------------------------------------------------------ */
const buscadorRespuestas = document.getElementById("buscadorRespuestas");

if (buscadorRespuestas) {
    buscadorRespuestas.addEventListener("input", () => {
        const termino = buscadorRespuestas.value.trim().toLowerCase();
        const filas = document.querySelectorAll("#tablaRespuestas tbody tr");

        filas.forEach(fila => {
            const esFilaVacia = fila.dataset.emptyRespuestas === "1";
            if (esFilaVacia) {
                fila.style.display = termino ? "none" : "";
                return;
            }

            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(termino) ? "" : "none";
        });
    });
}

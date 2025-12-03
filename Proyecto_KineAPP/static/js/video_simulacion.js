// video_simulacion.js

document.addEventListener("DOMContentLoaded", () => {
    const btns = document.querySelectorAll(".btn");
    const content = document.getElementById("contentWindow");

    // Obtenemos el template de ficha (puede ser null si no existe)
    const fichaTemplate = document.getElementById("ficha-template");

    // Cargar tópicos, preguntas y respuestas enviados por Django (json_script en la plantilla)
    let topicos = [];
    let preguntas = [];
    let respuestas = [];

    const topicosEl = document.getElementById("topicos-data");
    if (topicosEl) {
        try {
            topicos = JSON.parse(topicosEl.textContent);
        } catch (e) {
            topicos = [];
        }
    }

    const preguntasEl = document.getElementById("preguntas-data");
    if (preguntasEl) {
        try {
            preguntas = JSON.parse(preguntasEl.textContent);
        } catch (e) {
            preguntas = [];
        }
    }

    const respuestasEl = document.getElementById("respuestas-data");
    if (respuestasEl) {
        try {
            respuestas = JSON.parse(respuestasEl.textContent);
        } catch (e) {
            respuestas = [];
        }
    }

    const renderTopicos = () => {
        if (!topicos.length) {
            return "<h2>Tópicos</h2><p>No hay tópicos disponibles.</p>";
        }
        const items = topicos
            .map((t) => {
                const desc = t.descripcion ? " — " + t.descripcion : "";
                return `<li><a href="#" data-topico-id="${t.id}" class="topico-link"><strong>${t.nombre}</strong></a>${desc}</li>`;
            })
            .join("");
        return `<h2>Tópicos</h2><ul>${items}</ul>`;
    };

    const renderPreguntas = (topicoId = null) => {
        let lista = preguntas;
        if (topicoId !== null) {
            lista = preguntas.filter((p) => String(p.topico_id) === String(topicoId));
        }
        if (!lista.length) {
            return "<h2>Preguntas</h2><p>No hay preguntas para este tópico.</p>";
        }

        const bloques = lista
            .map((p) => {
                const opciones = respuestas
                    .filter((r) => String(r.pregunta_id) === String(p.id))
                    .map(
                        (r) =>
                            `<li>
                                <label>
                                    <input type="radio" name="preg-${p.id}" data-correct="${r.es_correcta}" />
                                    ${r.contenido}
                                </label>
                             </li>`
                    )
                    .join("");

                const opcionesHtml = opciones || "<li>No hay respuestas configuradas.</li>";

                return `
                    <div class="question-block" data-pid="${p.id}">
                        <p><strong>${p.pregunta}</strong></p>
                        <ul>${opcionesHtml}</ul>
                        <button class="check-answer" data-pid="${p.id}">Responder</button>
                        <div class="result" id="result-${p.id}" style="margin-top:8px;"></div>
                    </div>
                `;
            })
            .join("");

        return `<h2>Preguntas</h2>${bloques}`;
    };

    // 1. Definir el contenido de cada pestaña
    const sections = {
        resumen: "<h2>Resumen del caso</h2><p>Seleccione una sección.</p>",
        preguntas: renderPreguntas(),
        topicos: renderTopicos(),
        diagnostico: "<h2>Diagnóstico</h2><p>Aquí iría el diagnóstico...</p>",

        // Tomamos el HTML del formulario oculto si existe
        ficha: fichaTemplate
            ? fichaTemplate.innerHTML
            : "<p>No se encontró la ficha del paciente.</p>",
    };

    // 2. Función para cambiar de pestaña
    function setActive(section) {
        // Quitar clase active de todos los botones
        btns.forEach((b) => b.classList.remove("active"));

        // Poner clase active al botón presionado
        const activeBtn = document.querySelector(
            `.btn[data-section="${section}"]`
        );
        if (activeBtn) activeBtn.classList.add("active");

        // Inyectar el HTML correspondiente en el cuadro blanco
        if (sections[section]) {
            content.innerHTML = sections[section];
        } else {
            content.innerHTML = "<p>Sección no encontrada.</p>";
        }

        // Si estamos en tópicos, asignar click a los links para saltar a preguntas
        if (section === "topicos") {
            document.querySelectorAll(".topico-link").forEach((a) => {
                a.addEventListener("click", (e) => {
                    e.preventDefault();
                    const topicoId = a.dataset.topicoId;
                    // Cambiar sección a preguntas con las filtradas
                    btns.forEach((b) => b.classList.remove("active"));
                    const preguntasBtn = document.querySelector('.btn[data-section="preguntas"]');
                    if (preguntasBtn) preguntasBtn.classList.add("active");
                    content.innerHTML = renderPreguntas(topicoId);
                    attachPreguntaHandlers();
                });
            });
        }

        if (section === "preguntas") {
            attachPreguntaHandlers();
        }
    }

    function attachPreguntaHandlers() {
        document.querySelectorAll(".check-answer").forEach((btn) => {
            btn.addEventListener("click", () => {
                const pid = btn.dataset.pid;
                const radios = document.querySelectorAll(`input[name="preg-${pid}"]`);
                const resultEl = document.getElementById(`result-${pid}`);
                if (!radios.length) {
                    if (resultEl) resultEl.textContent = "No hay respuestas disponibles.";
                    return;
                }
                const selected = Array.from(radios).find((r) => r.checked);
                if (!selected) {
                    if (resultEl) resultEl.textContent = "Selecciona una opción.";
                    return;
                }
                const ok = selected.dataset.correct === "True" || selected.dataset.correct === "true";
                if (resultEl) {
                    resultEl.textContent = ok ? "Correcto" : "Incorrecto";
                    resultEl.style.color = ok ? "green" : "red";
                }
            });
        });
    }

    // 3. Asignar el evento click a los botones
    btns.forEach((btn) =>
        btn.addEventListener("click", () => {
            setActive(btn.dataset.section);
        })
    );

    // 4. Iniciar en la pestaña resumen por defecto
    setActive("resumen");

    // (Se eliminó el código del modal porque ya no se usa)
});

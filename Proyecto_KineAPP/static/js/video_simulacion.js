// video_simulacion.js

document.addEventListener("DOMContentLoaded", () => {

    const btns = document.querySelectorAll(".btn");
    const content = document.getElementById("contentWindow");

    // Obtenemos el template de ficha (puede ser null si no existe)
    const fichaTemplate = document.getElementById("ficha-template");

    // 1. Definir el contenido de cada pestaña
    const sections = {
        resumen: "<h2>Resumen del caso</h2><p>Seleccione una sección.</p>",
        preguntas: "<h2>Preguntas</h2><p>Aquí irían las preguntas...</p>",
        topicos: "<h2>Tópicos</h2><p>Aquí irían los tópicos...</p>",
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

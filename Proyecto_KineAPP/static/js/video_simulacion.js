document.addEventListener("DOMContentLoaded", () => {

    const btns = document.querySelectorAll('.btn');
    const content = document.getElementById('contentWindow');

    let currentTopic = null;

    const sections = {
        resumen: "<h2>Resumen del caso</h2><p>Seleccione una sección.</p>",
        preguntas: "<h2>Preguntas</h2>",
        topicos: "<h2>Tópicos</h2>",
        diagnostico: "<h2>Diagnóstico</h2>",
        ficha: "<h2>Ficha médica</h2>"
    };

    function setActive(section) {
        btns.forEach(b => b.classList.remove("active"));
        document.querySelector(`.btn[data-section="${section}"]`).classList.add("active");
        content.innerHTML = sections[section];
    }

    btns.forEach(btn => btn.addEventListener("click", () => {
        setActive(btn.dataset.section);
    }));

    setActive("resumen");

    // Modal
    const modal = document.getElementById("fichaModal");
    const btnFicha = document.querySelector(".btn[data-section='ficha']");
    const closeBtn = document.getElementById("closeFichaModal");

    btnFicha.addEventListener("click", () => modal.style.display = "flex");
    closeBtn.addEventListener("click", () => modal.style.display = "none");

    modal.addEventListener("click", e => {
        if (e.target === modal) modal.style.display = "none";
    });

});

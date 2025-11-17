document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector('input[name="rut"]');
    if (!input) return;

    input.addEventListener("input", function () {
        let value = input.value.toUpperCase().replace(/[^0-9K]/g, "");

        if (value.length <= 1) {
            input.value = value;
            return;
        }

        let cuerpo = value.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        let dv = value.slice(-1);
        input.value = `${cuerpo}-${dv}`;
    });
});

def validar_rut(rut: str) -> bool:
    """Valida el formato y dígito verificador del RUT chileno."""
    rut = rut.upper().replace("-", "").replace(".", "").strip()

    if not rut[:-1].isdigit() or len(rut) < 2:
        return False

    cuerpo, dv = rut[:-1], rut[-1]
    suma = 0
    multiplo = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    dv_calculado = 11 - (suma % 11)
    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    return dv == dv_calculado

def formatear_rut(rut: str) -> str:
    rut = rut.upper().replace("-", "").replace(".", "").strip()
    cuerpo, dv = rut[:-1], rut[-1]
    cuerpo = f"{int(cuerpo):,}".replace(",", ".")
    return f"{cuerpo}-{dv}"

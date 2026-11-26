
def validar_dominio(dominio):
    valido = True

    dominio = dominio.removesuffix(".")
    etiquetas = dominio.split(".")

    if len(etiquetas) < 2:
        valido = False

    if len(dominio) > 253:
        valido = False

    for etiqueta in etiquetas:
        if etiqueta == "":
            valido = False

        if etiqueta.startswith("-") or etiqueta.endswith("-"):
            valido = False

        if not etiqueta.isascii() or not etiqueta.replace("-", "").isalnum():
            valido = False

        if len(etiqueta) > 63:
            valido = False

    return valido

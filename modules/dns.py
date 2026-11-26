
import dns.resolver


def consultar_registro(dominio, tipo):
    registros = []
    estado = "ok"

    try:
        respuesta = dns.resolver.resolve(dominio, tipo)

        for registro in respuesta:
            registros.append(registro.to_text())

    except dns.resolver.NXDOMAIN:
        estado = "dominio_inexistente"

    except dns.resolver.NoAnswer:
        estado = "sin_registros"

    except dns.resolver.LifetimeTimeout:
        estado = "timeout"

    except dns.resolver.NoNameservers:
        estado = "error_servidores_dns"

    resultado = {
        "estado": estado,
        "registros": registros
    }

    return resultado


def consultar_dns(dominio):
    resultados = {}

    tipos = {
        "A": "Direcciones IPv4",
        "AAAA": "Direcciones IPv6",
        "MX": "Servidores de correo",
        "NS": "Servidores DNS",
        "TXT": "Registros TXT"
    }

    for tipo, descripcion in tipos.items():
        resultados[descripcion] = consultar_registro(dominio, tipo)

    return resultados

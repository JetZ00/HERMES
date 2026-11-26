
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


URL_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"


def consultar_rdap(dominio):
    resultado = {
        "estado": "error",
        "datos": {}
    }

    dominio = dominio.lower().removesuffix(".")
    servidor = buscar_servidor_rdap(dominio)

    if servidor["estado"] != "ok":
        resultado["estado"] = servidor["estado"]

    else:
        url = servidor["servidor"].rstrip("/") + "/domain/" + dominio

        try:
            peticion = Request(
                url,
                headers={
                    "User-Agent": "HERMES/0.2",
                    "Accept": "application/rdap+json"
                }
            )

            with urlopen(peticion, timeout=10) as respuesta:
                datos = json.load(respuesta)

            if isinstance(datos, dict):
                resultado["estado"] = "ok"
                resultado["datos"] = datos
            else:
                resultado["estado"] = "respuesta_invalida"

        except HTTPError as error:
            if error.code == 404:
                resultado["estado"] = "dominio_no_encontrado"
            else:
                resultado["estado"] = "error_http"
                resultado["codigo_http"] = error.code

        except URLError:
            resultado["estado"] = "error_conexion"

        except TimeoutError:
            resultado["estado"] = "timeout"

        except (ValueError, TypeError):
            resultado["estado"] = "respuesta_invalida"

    return resultado


def extraer_informacion_rdap(datos):
    informacion = {
        "dominio": datos.get("ldhName"),
        "registrador": None,
        "fecha_creacion": None,
        "fecha_expiracion": None,
        "ultima_modificacion": None,
        "estados": datos.get("status", []),
        "servidores_dns": []
    }

    # Extraer fechas de los eventos RDAP
    tipos_eventos = {
        "registration": "fecha_creacion",
        "expiration": "fecha_expiracion",
        "last changed": "ultima_modificacion"
    }

    for evento in datos.get("events", []):
        accion = evento.get("eventAction")
        fecha = evento.get("eventDate")

        if accion in tipos_eventos:
            campo = tipos_eventos[accion]
            informacion[campo] = fecha

    # Extraer servidores de nombres
    for servidor in datos.get("nameservers", []):
        nombre = servidor.get("ldhName")

        if nombre:
            informacion["servidores_dns"].append(nombre)

    # Identificar la entidad con rol de registrador
    for entidad in datos.get("entities", []):
        if "registrar" in entidad.get("roles", []):
            vcard = entidad.get("vcardArray", [])

            if len(vcard) >= 2:
                for propiedad in vcard[1]:
                    if propiedad[0] == "fn" and len(propiedad) >= 4:
                        informacion["registrador"] = propiedad[3]

    return informacion


def buscar_servidor_rdap(dominio):
    resultado = {
        "estado": "servidor_no_encontrado",
        "servidor": None
    }

    dominio = dominio.lower().removesuffix(".")

    try:
        peticion = Request(
            URL_BOOTSTRAP,
            headers={"User-Agent": "HERMES/0.2"}
        )

        with urlopen(peticion, timeout=10) as respuesta:
            datos = json.load(respuesta)

        coincidencia_mas_larga = -1

        for extensiones, servidores in datos["services"]:
            for extension in extensiones:

                coincide = (
                    dominio == extension
                    or dominio.endswith("." + extension)
                )

                if coincide and len(extension) > coincidencia_mas_larga:
                    servidores_https = [
                        servidor for servidor in servidores
                        if servidor.startswith("https://")
                    ]

                    if servidores_https:
                        coincidencia_mas_larga = len(extension)
                        resultado["estado"] = "ok"
                        resultado["servidor"] = servidores_https[0]

    except HTTPError:
        resultado["estado"] = "error_http"

    except URLError:
        resultado["estado"] = "error_conexion"

    except TimeoutError:
        resultado["estado"] = "timeout"

    except (ValueError, KeyError, TypeError):
        resultado["estado"] = "respuesta_invalida"

    return resultado

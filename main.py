import sys
import dns.resolver
import json
from pathlib import Path
from datetime import datetime, timezone

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

def guardar_json(datos, nombre_archivo):


  carpeta = Path("results")
  carpeta.mkdir(exist_ok=True)

  ruta_archivo = carpeta / f"{nombre_archivo}.json"
  
  with open(ruta_archivo, "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, indent=4, ensure_ascii=False)

# main.py

if __name__ == "__main__":
  if len(sys.argv)==2:
    dominio_objetivo = sys.argv[1]

    if validar_dominio(dominio_objetivo):

      print(f"""
      ===============================
              HERMES v0.1
                OSINT TOOL
      ===============================

      [+] Sistema iniciado correctamente
      
      [+] Objetivo: {dominio_objetivo}
      """)
      
      informacion_dns_objetivo = consultar_dns(dominio_objetivo)
      fecha = datetime.now(timezone.utc).isoformat(timespec="seconds")    
      
      informe = {
          "dominio": dominio_objetivo,
          "fecha_consulta": fecha,
          "dns": informacion_dns_objetivo
      }

      for descripcion, resultado in informacion_dns_objetivo.items():
        print(f"\n[+] {descripcion}:")

        estado = resultado["estado"]
        registros = resultado["registros"]

        if estado == "ok":
          for registro in registros:
            print(f"    {registro}")

        elif estado == "sin_registros":
          print("    No se encontraron registros")

        elif estado == "dominio_inexistente":
          print("    El dominio no existe")

        elif estado == "timeout":
          print("    Tiempo de espera agotado")

        elif estado == "error_servidores_dns":
          print("    Error de los servidores DNS")

      guardar_json(informe,f"{dominio_objetivo}_informe")

    else:
      print("ERROR: El dominio introducido no es válido")
      sys.exit(1)

  else:
    print("ERROR: Debes indicar exactamente un dominio")
    sys.exit(1)




import sys
from datetime import datetime, timezone

from modules.dns import consultar_dns
from modules.rdap import consultar_rdap, extraer_informacion_rdap
from modules.validation import validar_dominio
from modules.reports import guardar_json


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

# Programa principal
if __name__ == "__main__":

  if len(sys.argv) == 2:
    dominio_objetivo = sys.argv[1]

    if validar_dominio(dominio_objetivo):

      print(f"""
      ===============================
              HERMES v0.2
                OSINT TOOL
      ===============================

      [+] Sistema iniciado correctamente
      [+] Objetivo: {dominio_objetivo}
      """)

      # DNS Intelligence
      informacion_dns_objetivo = consultar_dns(dominio_objetivo)

      # RDAP Intelligence
      respuesta_rdap = consultar_rdap(dominio_objetivo)

      if respuesta_rdap["estado"] == "ok":
        informacion_rdap_objetivo = {
            "estado": "ok",
            "informacion": extraer_informacion_rdap(
                respuesta_rdap["datos"]
            )
        }
      else:
        informacion_rdap_objetivo = {
            "estado": respuesta_rdap["estado"],
            "informacion": {}
        }

      # Fecha e informe
      fecha = datetime.now(timezone.utc).isoformat(
          timespec="seconds"
      )

      informe = {
          "dominio": dominio_objetivo,
          "fecha_consulta": fecha,
          "dns": informacion_dns_objetivo,
          "rdap": informacion_rdap_objetivo
      }

      # Mostrar resultados DNS
      print("\n========== DNS Intelligence ==========")

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

      # Mostrar resultados RDAP
      print("\n========== RDAP Intelligence ==========")

      if informacion_rdap_objetivo["estado"] == "ok":

        datos_rdap = informacion_rdap_objetivo["informacion"]

        print(f"\n[+] Dominio: {datos_rdap['dominio']}")
        print(f"[+] Registrador: {datos_rdap['registrador']}")
        print(f"[+] Fecha de creación: {datos_rdap['fecha_creacion']}")
        print(f"[+] Fecha de expiración: {datos_rdap['fecha_expiracion']}")
        print(f"[+] Última modificación: {datos_rdap['ultima_modificacion']}")

        print("\n[+] Estados del dominio:")
        for estado in datos_rdap["estados"]:
          print(f"    {estado}")

        print("\n[+] Servidores de nombres:")
        for servidor in datos_rdap["servidores_dns"]:
          print(f"    {servidor}")

      else:
        print(
            f"[-] Consulta RDAP: "
            f"{informacion_rdap_objetivo['estado']}"
        )

      # Guardar informe una sola vez
      guardar_json(informe, f"{dominio_objetivo}_informe")

    else:
      print("ERROR: El dominio introducido no es válido")
      sys.exit(1)

  else:
    print("ERROR: Debes indicar exactamente un dominio")
    sys.exit(1)

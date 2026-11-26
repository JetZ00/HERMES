
import unittest
import json
import tempfile

from pathlib import Path
from unittest.mock import patch
from modules.reports import guardar_json


class TestReportes(unittest.TestCase):

    def test_crear_informe_json(self):

        datos = {
            "dominio": "example.com",
            "fecha_consulta": "2026-11-13T18:00:00+00:00",
            "dns": {
                "Direcciones IPv4": {
                    "estado": "ok",
                    "registros": ["192.0.2.1"]
                },
                "Direcciones IPv6": {
                    "estado": "sin_registros",
                    "registros": []
                }
            }
        }

        with tempfile.TemporaryDirectory() as directorio:
            ruta_resultados = Path(directorio) / "results"

            with patch("modules.reports.Path", return_value=ruta_resultados):

                guardar_json(datos, "example.com_informe")

            ruta = ruta_resultados / "example.com_informe.json"

            self.assertTrue(ruta.exists())

            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)

            self.assertEqual(contenido, datos)


    def test_conservar_caracteres_especiales(self):

        datos = {
            "descripcion": "Información de investigación DNS"
        }

        with tempfile.TemporaryDirectory() as directorio:
            ruta_resultados = Path(directorio) / "results"

            with patch("modules.reports.Path", return_value=ruta_resultados):

                guardar_json(datos, "prueba_unicode")

            ruta = ruta_resultados / "prueba_unicode.json"

            contenido = ruta.read_text(encoding="utf-8")

            self.assertIn("Información", contenido)
            self.assertNotIn("\\u00f3", contenido)


if __name__ == "__main__":
    unittest.main()

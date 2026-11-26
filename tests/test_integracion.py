
import unittest
import json
import sys
import os
import runpy
import tempfile
import dns.resolver

from pathlib import Path
from unittest.mock import patch, MagicMock


RUTA_MAIN = Path(__file__).resolve().parents[1] / "main.py"


class TestIntegracion(unittest.TestCase):

    @patch("modules.rdap.consultar_rdap")
    @patch("dns.resolver.resolve")
    def test_informe_dns_y_rdap(self, mock_dns, mock_rdap):

        # Simular respuesta DNS
        registro = MagicMock()
        registro.to_text.return_value = "192.0.2.1"

        def resolver_simulado(dominio, tipo):
            if tipo == "A":
                return [registro]

            raise dns.resolver.NoAnswer()

        mock_dns.side_effect = resolver_simulado

        # Simular respuesta RDAP
        mock_rdap.return_value = {
            "estado": "ok",
            "datos": {
                "ldhName": "EXAMPLE.COM",
                "status": ["active"],
                "events": [
                    {
                        "eventAction": "registration",
                        "eventDate": "2000-01-01T00:00:00Z"
                    }
                ],
                "nameservers": [
                    {"ldhName": "NS1.EXAMPLE.COM"}
                ],
                "entities": []
            }
        }

        # Ejecutar HERMES en una carpeta temporal
        with tempfile.TemporaryDirectory() as directorio:

            ruta_anterior = Path.cwd()

            try:
                os.chdir(directorio)

                with patch.object(
                    sys, "argv", ["main.py", "example.com"]
                ):
                    runpy.run_path(
                        str(RUTA_MAIN),
                        run_name="__main__"
                    )

                # Comprobar el archivo generado
                ruta_informe = (
                    Path("results") / "example.com_informe.json"
                )

                self.assertTrue(ruta_informe.exists())

                with open(
                    ruta_informe, "r", encoding="utf-8"
                ) as archivo:
                    informe = json.load(archivo)

                # Comprobar DNS
                self.assertIn("dns", informe)

                self.assertEqual(
                    informe["dns"]["Direcciones IPv4"]["registros"],
                    ["192.0.2.1"]
                )

                # Comprobar RDAP
                self.assertIn("rdap", informe)

                self.assertEqual(
                    informe["rdap"]["estado"],
                    "ok"
                )

                self.assertEqual(
                    informe["rdap"]["informacion"]["dominio"],
                    "EXAMPLE.COM"
                )

                self.assertEqual(
                    informe["rdap"]["informacion"]["fecha_creacion"],
                    "2000-01-01T00:00:00Z"
                )

                mock_rdap.assert_called_once_with("example.com")

            finally:
                os.chdir(ruta_anterior)


if __name__ == "__main__":
    unittest.main()


import unittest
import json

from unittest.mock import patch, MagicMock
from urllib.error import HTTPError

from modules.rdap import (
    buscar_servidor_rdap,
    consultar_rdap,
    extraer_informacion_rdap
)


class TestRDAP(unittest.TestCase):

    @patch("modules.rdap.json.load")
    @patch("modules.rdap.urlopen")
    def test_descubrir_servidor(self, mock_urlopen, mock_json):

        mock_json.return_value = {
            "services": [
                [
                    ["com"],
                    ["https://rdap.example.com/"]
                ]
            ]
        }

        resultado = buscar_servidor_rdap("google.com")

        self.assertEqual(resultado["estado"], "ok")
        self.assertEqual(
            resultado["servidor"],
            "https://rdap.example.com/"
        )


    @patch("modules.rdap.json.load")
    @patch("modules.rdap.urlopen")
    def test_extension_no_encontrada(self, mock_urlopen, mock_json):

        mock_json.return_value = {
            "services": [
                [
                    ["com"],
                    ["https://rdap.example.com/"]
                ]
            ]
        }

        resultado = buscar_servidor_rdap("example.invalid")

        self.assertEqual(
            resultado["estado"],
            "servidor_no_encontrado"
        )


    @patch("modules.rdap.json.load")
    @patch("modules.rdap.urlopen")
    @patch("modules.rdap.buscar_servidor_rdap")
    def test_consulta_correcta(
        self, mock_servidor, mock_urlopen, mock_json
    ):

        mock_servidor.return_value = {
            "estado": "ok",
            "servidor": "https://rdap.example.com/"
        }

        mock_json.return_value = {
            "ldhName": "EXAMPLE.COM",
            "status": ["active"]
        }

        resultado = consultar_rdap("example.com")

        self.assertEqual(resultado["estado"], "ok")
        self.assertEqual(
            resultado["datos"]["ldhName"],
            "EXAMPLE.COM"
        )


    @patch("modules.rdap.urlopen")
    @patch("modules.rdap.buscar_servidor_rdap")
    def test_dominio_no_encontrado(
        self, mock_servidor, mock_urlopen
    ):

        mock_servidor.return_value = {
            "estado": "ok",
            "servidor": "https://rdap.example.com/"
        }

        mock_urlopen.side_effect = HTTPError(
            url="https://rdap.example.com/domain/example.com",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=None
        )

        resultado = consultar_rdap("example.com")

        self.assertEqual(
            resultado["estado"],
            "dominio_no_encontrado"
        )


    def test_extraer_informacion(self):

        datos = {
            "ldhName": "EXAMPLE.COM",
            "status": ["active"],
            "events": [
                {
                    "eventAction": "registration",
                    "eventDate": "2000-01-01T00:00:00Z"
                },
                {
                    "eventAction": "expiration",
                    "eventDate": "2030-01-01T00:00:00Z"
                }
            ],
            "nameservers": [
                {"ldhName": "NS1.EXAMPLE.COM"}
            ],
            "entities": [
                {
                    "roles": ["registrar"],
                    "vcardArray": [
                        "vcard",
                        [
                            ["fn", {}, "text", "Example Registrar"]
                        ]
                    ]
                }
            ]
        }

        resultado = extraer_informacion_rdap(datos)

        self.assertEqual(resultado["dominio"], "EXAMPLE.COM")
        self.assertEqual(resultado["registrador"], "Example Registrar")
        self.assertEqual(
            resultado["fecha_creacion"],
            "2000-01-01T00:00:00Z"
        )
        self.assertEqual(
            resultado["fecha_expiracion"],
            "2030-01-01T00:00:00Z"
        )
        self.assertEqual(
            resultado["servidores_dns"],
            ["NS1.EXAMPLE.COM"]
        )


    def test_campos_ausentes(self):

        resultado = extraer_informacion_rdap({})

        self.assertIsNone(resultado["dominio"])
        self.assertIsNone(resultado["registrador"])
        self.assertIsNone(resultado["fecha_creacion"])
        self.assertIsNone(resultado["fecha_expiracion"])
        self.assertEqual(resultado["servidores_dns"], [])
        self.assertEqual(resultado["estados"], [])


if __name__ == "__main__":
    unittest.main()

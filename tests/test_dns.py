
import unittest
import dns.resolver

from unittest.mock import patch, MagicMock
from main import consultar_registro, consultar_dns


class TestDNS(unittest.TestCase):

    @patch("main.dns.resolver.resolve")
    def test_consulta_ipv4(self, mock_resolve):
        registro = MagicMock()
        registro.to_text.return_value = "192.0.2.1"

        mock_resolve.return_value = [registro]

        resultado = consultar_registro("example.com", "A")

        self.assertEqual(resultado["estado"], "ok")
        self.assertEqual(resultado["registros"], ["192.0.2.1"])

        mock_resolve.assert_called_once_with("example.com", "A")


    @patch("main.dns.resolver.resolve")
    def test_varios_registros_ipv4(self, mock_resolve):
        registro1 = MagicMock()
        registro1.to_text.return_value = "192.0.2.1"

        registro2 = MagicMock()
        registro2.to_text.return_value = "192.0.2.2"

        mock_resolve.return_value = [registro1, registro2]

        resultado = consultar_registro("example.com", "A")

        self.assertEqual(resultado["estado"], "ok")
        self.assertEqual(
            resultado["registros"],
            ["192.0.2.1", "192.0.2.2"]
        )


    @patch("main.dns.resolver.resolve")
    def test_registros_mx(self, mock_resolve):
        registro = MagicMock()
        registro.to_text.return_value = "10 mail.example.com."

        mock_resolve.return_value = [registro]

        resultado = consultar_registro("example.com", "MX")

        self.assertEqual(resultado["estado"], "ok")
        self.assertEqual(resultado["registros"], ["10 mail.example.com."])


    @patch("main.dns.resolver.resolve")
    def test_dominio_inexistente(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NXDOMAIN()

        resultado = consultar_registro("example.com", "A")

        self.assertEqual(resultado["estado"], "dominio_inexistente")
        self.assertEqual(resultado["registros"], [])


    @patch("main.dns.resolver.resolve")
    def test_sin_registros_ipv6(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NoAnswer()

        resultado = consultar_registro("example.com", "AAAA")

        self.assertEqual(resultado["estado"], "sin_registros")
        self.assertEqual(resultado["registros"], [])


    @patch("main.dns.resolver.resolve")
    def test_error_servidores_dns(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NoNameservers()

        resultado = consultar_registro("example.com", "NS")

        self.assertEqual(resultado["estado"], "error_servidores_dns")
        self.assertEqual(resultado["registros"], [])


    @patch("main.dns.resolver.resolve")
    def test_timeout_dns(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.LifetimeTimeout()

        resultado = consultar_registro("example.com", "TXT")

        self.assertEqual(resultado["estado"], "timeout")
        self.assertEqual(resultado["registros"], [])


    @patch("main.consultar_registro")
    def test_consultar_todos_los_tipos(self, mock_consultar):
        mock_consultar.return_value = {
            "estado": "ok",
            "registros": ["dato_simulado"]
        }

        resultado = consultar_dns("example.com")

        self.assertEqual(len(resultado), 5)
        self.assertEqual(mock_consultar.call_count, 5)

        self.assertIn("Direcciones IPv4", resultado)
        self.assertIn("Direcciones IPv6", resultado)
        self.assertIn("Servidores de correo", resultado)
        self.assertIn("Servidores DNS", resultado)
        self.assertIn("Registros TXT", resultado)


if __name__ == "__main__":
    unittest.main()

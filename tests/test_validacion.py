
import unittest
from main import validar_dominio

class TestValidacion(unittest.TestCase):

    def test_dominio_valido(self):
        self.assertTrue(validar_dominio("google.com"))

    def test_subdominio_valido(self):
        self.assertTrue(validar_dominio("mail.google.com"))

    def test_punto_final_valido(self):
        self.assertTrue(validar_dominio("google.com."))

    def test_sin_punto(self):
        self.assertFalse(validar_dominio("localhost"))

    def test_puntos_consecutivos(self):
        self.assertFalse(validar_dominio("google..com"))

    def test_guion_inicial(self):
        self.assertFalse(validar_dominio("-google.com"))

    def test_guion_final(self):
        self.assertFalse(validar_dominio("google-.com"))

    def test_espacios(self):
        self.assertFalse(validar_dominio("hola mundo.com"))

    def test_url_en_lugar_de_dominio(self):
        self.assertFalse(validar_dominio("google.com/archivo"))

    def test_etiqueta_demasiado_larga(self):
        dominio = "a" * 64 + ".com"
        self.assertFalse(validar_dominio(dominio))

    def test_dominio_demasiado_largo(self):
        dominio = "a" * 63 + "." + "b" * 63 + "." + "c" * 63 + "." + "d" * 62 + ".com"
        self.assertFalse(validar_dominio(dominio))


if __name__ == "__main__":
    unittest.main()

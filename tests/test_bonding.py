"""Pruebas del análisis de enlaces (valencia y polaridad)."""
import unittest

from ampa.chemistry.bonding import analizar_enlaces, polaridad
from ampa.chemistry.molecules import Molecula


class TestPolaridad(unittest.TestCase):
    def test_clasificacion(self):
        self.assertEqual(polaridad(0.3), "covalente no polar")
        self.assertEqual(polaridad(1.0), "covalente polar")
        self.assertEqual(polaridad(2.2), "iónico")


class TestAnalisis(unittest.TestCase):
    def test_agua_saturada_y_polar(self):
        agua = Molecula("agua", ["O", "H", "H"], [(0, 1, 1), (0, 2, 1)])
        r = analizar_enlaces(agua)
        self.assertEqual(r["atomos"][0]["valencia_tipica"], 2)
        self.assertEqual(r["atomos"][0]["estado"], "saturado")
        self.assertEqual(r["enlaces"][0]["polaridad"], "covalente polar")
        self.assertTrue(r["estable"])

    def test_metano_no_polar(self):
        ch4 = Molecula("metano", ["C", "H", "H", "H", "H"], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)])
        r = analizar_enlaces(ch4)
        self.assertEqual(r["atomos"][0]["estado"], "saturado")
        self.assertEqual(r["enlaces"][0]["polaridad"], "covalente no polar")

    def test_sobreenlazado_no_estable(self):
        m = Molecula("x", ["O", "H", "H", "H"], [(0, 1, 1), (0, 2, 1), (0, 3, 1)])
        r = analizar_enlaces(m)
        self.assertEqual(r["atomos"][0]["estado"], "sobreenlazado")
        self.assertFalse(r["estable"])


if __name__ == "__main__":
    unittest.main()

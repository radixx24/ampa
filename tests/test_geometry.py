"""Pruebas de la geometría 3D (layout por fuerzas)."""
import math
import unittest

from ampa.chemistry.geometry import geometria_3d
from ampa.chemistry.molecules import Molecula


class TestGeometria(unittest.TestCase):
    def test_una_coordenada_por_atomo(self):
        g = geometria_3d(Molecula("agua", ["O", "H", "H"], [(0, 1, 1), (0, 2, 1)]))
        self.assertEqual(len(g), 3)
        self.assertEqual(set(g[0]), {"el", "x", "y", "z"})

    def test_determinista(self):
        m = Molecula("co2", ["C", "O", "O"], [(0, 1, 2), (0, 2, 2)])
        self.assertEqual(geometria_3d(m), geometria_3d(m))

    def test_molecula_vacia(self):
        self.assertEqual(geometria_3d(Molecula()), [])

    def test_enlace_a_distancia_razonable(self):
        g = geometria_3d(Molecula("h2", ["H", "H"], [(0, 1, 1)]))
        d = math.dist(
            (g[0]["x"], g[0]["y"], g[0]["z"]), (g[1]["x"], g[1]["y"], g[1]["z"])
        )
        self.assertTrue(0.8 < d < 4.0)


if __name__ == "__main__":
    unittest.main()

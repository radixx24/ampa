"""Pruebas del editor de carbono: grupos funcionales y reacciones."""
import unittest

from ampa.chemistry.groups import grupos_funcionales
from ampa.chemistry.molecules import Molecula
from ampa.chemistry.reactions import reacciones

METANO = Molecula("metano", ["C", "H", "H", "H", "H"], [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)])
ETENO = Molecula("eteno", ["C", "C", "H", "H", "H", "H"], [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)])
ETANOL = Molecula(
    "etanol",
    ["C", "C", "O", "H", "H", "H", "H", "H", "H"],
    [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 4, 1), (0, 5, 1), (0, 6, 1), (1, 7, 1), (1, 8, 1)],
)
ACETICO = Molecula(
    "ácido acético",
    ["C", "C", "O", "O", "H", "H", "H", "H"],
    [(0, 1, 1), (1, 2, 2), (1, 3, 1), (3, 4, 1), (0, 5, 1), (0, 6, 1), (0, 7, 1)],
)


class TestGrupos(unittest.TestCase):
    def test_alqueno(self):
        self.assertIn("alqueno", grupos_funcionales(ETENO))

    def test_alcohol(self):
        self.assertIn("alcohol", grupos_funcionales(ETANOL))

    def test_acido_no_cuenta_su_oh_como_alcohol(self):
        grupos = grupos_funcionales(ACETICO)
        self.assertIn("ácido carboxílico", grupos)
        self.assertNotIn("alcohol", grupos)

    def test_metano_sin_grupos(self):
        self.assertEqual(grupos_funcionales(METANO), [])


class TestReacciones(unittest.TestCase):
    def test_combustion_metano_balanceada(self):
        ecuaciones = [r.ecuacion for r in reacciones(METANO)]
        self.assertIn("CH4 + 2 O2 → CO2 + 2 H2O", ecuaciones)

    def test_combustion_etanol_balanceada(self):
        ecuaciones = [r.ecuacion for r in reacciones(ETANOL)]
        self.assertIn("C2H6O + 3 O2 → 2 CO2 + 3 H2O", ecuaciones)

    def test_hidrogenacion_de_alqueno(self):
        self.assertIn("hidrogenación", [r.tipo for r in reacciones(ETENO)])

    def test_neutralizacion_de_acido(self):
        self.assertIn("neutralización", [r.tipo for r in reacciones(ACETICO)])


if __name__ == "__main__":
    unittest.main()

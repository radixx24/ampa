"""Pruebas del modelo de moléculas y la persistencia de compuestos."""
import tempfile
import unittest
from pathlib import Path

from ampa.chemistry.molecules import Molecula, cargar_compuestos, guardar_compuesto

AGUA = Molecula(nombre="agua", atomos=["O", "H", "H"], enlaces=[(0, 1, 1), (0, 2, 1)])
CO2 = Molecula(
    nombre="dióxido de carbono", atomos=["C", "O", "O"], enlaces=[(0, 1, 2), (0, 2, 2)]
)


class TestMolecula(unittest.TestCase):
    def test_formula_composicion_y_masa(self):
        self.assertEqual(AGUA.formula(), "H2O")
        self.assertEqual(AGUA.composicion(), {"O": 1, "H": 2})
        self.assertAlmostEqual(AGUA.masa_molar(), 18.015, places=2)
        self.assertEqual(CO2.formula(), "CO2")

    def test_formula_hill_con_carbono(self):
        etano = Molecula(atomos=["C", "C", "H", "H", "H", "H", "H", "H"], enlaces=[(0, 1, 1)])
        self.assertEqual(etano.formula(), "C2H6")  # C, luego H

    def test_validar_detecta_errores(self):
        with self.assertRaises(ValueError):
            Molecula(atomos=["O", "H"], enlaces=[(0, 5, 1)]).validar()  # índice
        with self.assertRaises(ValueError):
            Molecula(atomos=["O", "H"], enlaces=[(0, 1, 4)]).validar()  # orden
        with self.assertRaises(ValueError):
            Molecula(atomos=["Xx"], enlaces=[]).validar()  # elemento

    def test_roundtrip_y_persistencia(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "compuestos.jsonl"
            guardar_compuesto(AGUA, ruta)
            guardar_compuesto(CO2, ruta)
            cargados = cargar_compuestos(ruta)
            self.assertEqual([m.formula() for m in cargados], ["H2O", "CO2"])
            self.assertEqual(cargados[0].nombre, "agua")


if __name__ == "__main__":
    unittest.main()

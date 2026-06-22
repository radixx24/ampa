"""Pruebas de compatibilidad entre elementos (cargas + ΔEN + termo)."""
import unittest

from ampa.chemistry.compatibility import compatibilidad


class TestCompatibilidad(unittest.TestCase):
    def test_sodio_cloro_ionico(self):
        res = compatibilidad("Na", "Cl")
        self.assertTrue(res["ok"])
        self.assertEqual(res["tipo_enlace"], "iónico")
        self.assertEqual(res["producto"], "NaCl")
        self.assertEqual(res["reactividad"], "muy alta")
        self.assertTrue(res["termo"]["espontanea"])  # formación favorable

    def test_aluminio_oxigeno_aspa(self):
        # Al³⁺ + O²⁻ → Al2O3 (subíndices cruzados).
        res = compatibilidad("Al", "O")
        self.assertEqual(res["producto"], "Al2O3")
        self.assertEqual(res["tipo_enlace"], "iónico")

    def test_calcio_oxigeno_reduce(self):
        # Ca²⁺ + O²⁻ → CaO (se reduce 2:2 a 1:1).
        res = compatibilidad("calcio", "oxígeno")  # acepta nombres
        self.assertEqual(res["producto"], "CaO")

    def test_carbono_oxigeno_covalente(self):
        res = compatibilidad("C", "O")
        self.assertIn("covalente", res["tipo_enlace"])
        self.assertIsNone(res["producto"])

    def test_gas_noble_inerte(self):
        res = compatibilidad("Ne", "F")
        self.assertEqual(res["tipo_enlace"], "inerte")
        self.assertEqual(res["reactividad"], "nula")

    def test_dos_metales_aleacion(self):
        res = compatibilidad("Fe", "Cu")
        self.assertEqual(res["tipo_enlace"], "metálico")

    def test_desconocido(self):
        res = compatibilidad("Xx", "O")
        self.assertFalse(res["ok"])


if __name__ == "__main__":
    unittest.main()

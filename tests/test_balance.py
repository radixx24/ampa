"""Pruebas del balanceo general de ecuaciones (espacio nulo, Fraction)."""
import unittest

from ampa.chemistry.balance import balancear, ecuacion


class TestBalance(unittest.TestCase):
    def test_combustion_metano(self):
        coefs = balancear(["CH4", "O2"], ["CO2", "H2O"])
        self.assertEqual(coefs, ([1, 2], [1, 2]))

    def test_formacion_agua(self):
        coefs = balancear(["H2", "O2"], ["H2O"])
        self.assertEqual(coefs, ([2, 1], [2]))

    def test_sodio_agua(self):
        coefs = balancear(["Na", "H2O"], ["NaOH", "H2"])
        self.assertEqual(coefs, ([2, 2], [2, 1]))

    def test_oxido_hidratado_colapsa(self):
        # Na2O + H2O → 2 NaOH (el isómero estequiométrico se reacomoda)
        coefs = balancear(["Na2O", "H2O"], ["NaOH"])
        self.assertEqual(coefs, ([1, 1], [2]))

    def test_redox_hierro(self):
        coefs = balancear(["Fe", "O2"], ["Fe2O3"])
        self.assertEqual(coefs, ([4, 3], [2]))

    def test_amoniaco(self):
        coefs = balancear(["N2", "H2"], ["NH3"])
        self.assertEqual(coefs, ([1, 3], [2]))

    def test_imposible_devuelve_none(self):
        # No se conserva el oxígeno: no hay solución.
        self.assertIsNone(balancear(["CH4", "O2"], ["CO2"]))

    def test_formula_invalida_none(self):
        self.assertIsNone(balancear(["Xx2"], ["Yy"]))

    def test_ecuacion_formato(self):
        coefs = balancear(["CH4", "O2"], ["CO2", "H2O"])
        self.assertEqual(
            ecuacion(["CH4", "O2"], ["CO2", "H2O"], coefs),
            "CH4 + 2 O2 → CO2 + 2 H2O",
        )


if __name__ == "__main__":
    unittest.main()

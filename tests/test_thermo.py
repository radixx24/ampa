"""Pruebas de termodinámica (Energía Libre de Gibbs como umbral)."""
import unittest

from ampa.chemistry.thermo import evaluar, gibbs, proyectar


class TestGibbs(unittest.TestCase):
    def test_formula(self):
        # ΔG = ΔH − T·ΔS, con ΔS en J/K → kJ.
        self.assertAlmostEqual(gibbs(-100.0, 200.0, 300.0), -160.0, places=3)

    def test_signo(self):
        self.assertLess(gibbs(-50.0, 10.0, 298.15), 0)


class TestProyectar(unittest.TestCase):
    def test_sodio_agua_muy_negativa(self):
        # El ejemplo clásico: Na + agua libera mucha energía → ΔG ≪ 0.
        res = proyectar(["Na", "H2O"], ["NaOH", "H2"])
        self.assertTrue(res["ok"])
        self.assertTrue(res["espontanea"])
        self.assertLess(res["dG"], -200)
        self.assertEqual(res["veredicto"], "espontánea")

    def test_oxido_hidratado_colapsa_a_hidroxido(self):
        # Na2O·H2O en papel → la naturaleza elige 2 NaOH (más estable): ΔG < 0.
        res = proyectar(["Na2O", "H2O"], ["NaOH"])
        self.assertTrue(res["ok"])
        self.assertTrue(res["espontanea"])
        self.assertEqual(res["ecuacion"], "Na2O + H2O → 2 NaOH")

    def test_combustion_metano_espontanea(self):
        res = proyectar(["CH4", "O2"], ["CO2", "H2O"])
        self.assertTrue(res["espontanea"])
        self.assertLess(res["dH"], 0)  # exotérmica

    def test_temperatura_de_cruce(self):
        # CaCO3 → CaO + CO2 es endotérmica con ΔS>0: espontánea a alta T.
        frio = proyectar(["CaCO3"], ["CaO", "CO2"], T=298.15)
        caliente = proyectar(["CaCO3"], ["CaO", "CO2"], T=1500.0)
        self.assertFalse(frio["espontanea"])
        self.assertTrue(caliente["espontanea"])
        self.assertIsNotNone(frio["t_cruce"])

    def test_sin_datos_reporta_faltan(self):
        res = proyectar(["CH4", "O2"], ["XeF6"])  # sin datos / no balancea
        self.assertFalse(res["ok"])

    def test_no_balanceable(self):
        res = proyectar(["CH4", "O2"], ["CO2"])
        self.assertFalse(res["ok"])


if __name__ == "__main__":
    unittest.main()

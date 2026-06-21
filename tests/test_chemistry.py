"""Pruebas del reconocimiento químico (chemistry)."""
import unittest

from ampa.chemistry import identificar
from ampa.chemistry.formulas import composicion_valida, parsear_formula


class TestFormulas(unittest.TestCase):
    def test_parseo_con_parentesis(self):
        self.assertEqual(parsear_formula("H2O"), {"H": 2, "O": 1})
        self.assertEqual(parsear_formula("CO2"), {"C": 1, "O": 2})
        self.assertEqual(parsear_formula("Ca(OH)2"), {"Ca": 1, "O": 2, "H": 2})

    def test_valida_simbolos_reales(self):
        self.assertEqual(composicion_valida("NaCl"), {"Na": 1, "Cl": 1})
        self.assertIsNone(composicion_valida("Xy2"))  # Xy no es un elemento
        self.assertIsNone(composicion_valida("H2O)"))  # mal formada


class TestIdentificar(unittest.TestCase):
    def test_compuestos_por_formula(self):
        r = identificar("La molécula de H2O y el CO2 son clave.")
        formulas = {c.formula for c in r.compuestos}
        self.assertIn("H2O", formulas)
        self.assertIn("CO2", formulas)
        agua = next(c for c in r.compuestos if c.formula == "H2O")
        self.assertEqual(agua.composicion, {"H": 2, "O": 1})
        self.assertEqual(agua.nombre, "agua")  # nombrado desde el diccionario

    def test_elementos_por_nombre(self):
        r = identificar("El oxígeno y el sodio reaccionan.")
        simbolos = {e.simbolo for e in r.elementos}
        self.assertIn("O", simbolos)
        self.assertIn("Na", simbolos)
        oxigeno = next(e for e in r.elementos if e.simbolo == "O")
        self.assertEqual(oxigeno.numero_atomico, 8)

    def test_compuesto_por_nombre(self):
        r = identificar("El agua y el dióxido de carbono.")
        self.assertEqual({c.formula for c in r.compuestos}, {"H2O", "CO2"})

    def test_elemento_dentro_de_compuesto_no_se_duplica(self):
        r = identificar("El cloruro de sodio es común.")
        self.assertTrue(any(c.formula == "NaCl" for c in r.compuestos))
        self.assertFalse(any(e.simbolo == "Na" for e in r.elementos))

    def test_sin_falsos_positivos_en_texto_comun(self):
        r = identificar("El gato corre rápido por el parque al anochecer.")
        self.assertFalse(r.hay())


if __name__ == "__main__":
    unittest.main()

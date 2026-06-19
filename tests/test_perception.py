"""Pruebas de la capa de percepción."""
import unittest

from ampa.perception import events as E
from ampa.perception import perceive
from ampa.perception.classifier import clasificar


class TestClasificador(unittest.TestCase):
    def test_quimica(self):
        dom, terminos = clasificar("¿Qué es un enlace covalente?")
        self.assertEqual(dom, E.QUIMICA)
        self.assertIn("enlace", terminos)
        self.assertIn("covalent", terminos)

    def test_filosofia(self):
        dom, terminos = clasificar("Explica la epistemología de Kant")
        self.assertEqual(dom, E.FILOSOFIA)

    def test_operacion(self):
        dom, _ = clasificar("compila el proyecto con cmake")
        self.assertEqual(dom, E.OPERACION)

    def test_documentacion(self):
        dom, _ = clasificar("revisa el changelog y el roadmap")
        self.assertEqual(dom, E.DOCUMENTACION)

    def test_general_sin_coincidencias(self):
        dom, terminos = clasificar("hola, buenos dias")
        self.assertEqual(dom, E.GENERAL)
        self.assertEqual(terminos, [])

    def test_sin_acentos_equivale(self):
        con = clasificar("reacción química")[0]
        sin = clasificar("reaccion quimica")[0]
        self.assertEqual(con, sin)
        self.assertEqual(con, E.QUIMICA)


class TestPerceive(unittest.TestCase):
    def test_evento_valido(self):
        ev = perceive("¿Qué es un ácido fuerte?")
        self.assertIn(ev.tipo, E.TIPOS)
        self.assertIn(ev.dominio_probable, E.DOMINIOS)
        self.assertIn(ev.riesgo_operativo, E.RIESGOS)
        self.assertEqual(ev.dominio_probable, E.QUIMICA)
        self.assertEqual(ev.riesgo_operativo, E.BAJO)

    def test_pregunta_general_breve_no_se_guarda(self):
        ev = perceive("hola?")
        self.assertEqual(ev.dominio_probable, E.GENERAL)
        self.assertFalse(ev.guardar_en_memoria)

    def test_quimica_se_guarda(self):
        ev = perceive("Describe la oxidación del hierro")
        self.assertTrue(ev.guardar_en_memoria)

    def test_comando_riesgo_alto_con_archivo(self):
        ev = perceive("corrige el archivo docs/readme.md")
        self.assertEqual(ev.tipo, E.COMANDO)
        self.assertEqual(ev.riesgo_operativo, E.ALTO)
        self.assertIn("docs/readme.md", ev.archivos_relacionados)

    def test_deteccion_de_archivo(self):
        ev = perceive("revisa main.py por favor")
        self.assertIn("main.py", ev.archivos_relacionados)

    def test_tipo_explicito_se_respeta(self):
        ev = perceive("el enlace es covalente", tipo=E.DECISION)
        self.assertEqual(ev.tipo, E.DECISION)

    def test_as_yaml_contiene_campos(self):
        ev = perceive("¿Qué es un mol?")
        salida = ev.as_yaml()
        self.assertIn("evento:", salida)
        self.assertIn("dominio_probable:", salida)
        self.assertIn("riesgo_operativo:", salida)


if __name__ == "__main__":
    unittest.main()

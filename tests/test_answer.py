"""Pruebas de la capa de respuesta (answer.responder)."""
import tempfile
import unittest
from pathlib import Path

from ampa.answer import responder
from ampa.memory import ingerir

QUIMICA = "El enlace covalente se forma cuando dos atomos comparten electrones de valencia."
FILOSOFIA = "La epistemologia de Kant distingue el fenomeno de la cosa en si misma."


class TestResponder(unittest.TestCase):
    def _memoria(self, d):
        ruta = Path(d) / "frag.jsonl"
        ingerir(texto=f"{QUIMICA}\n\n{FILOSOFIA}", fuente="apuntes.md", ruta=ruta)
        return ruta

    def test_responde_con_cita_y_dominio(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = self._memoria(d)
            resp = responder("que es el enlace covalente", ruta=ruta)
            self.assertTrue(resp.hay_evidencia())
            self.assertEqual(resp.dominio, "quimica")
            self.assertIn("covalente", resp.texto())
            self.assertIn("[apuntes.md#0]", resp.texto())
            self.assertIn("[apuntes.md#0]", resp.fuentes())

    def test_sin_evidencia_es_honesto(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "vacia.jsonl"  # no existe → memoria vacía
            resp = responder("algo que no esta en los apuntes", ruta=ruta)
            self.assertFalse(resp.hay_evidencia())
            self.assertIn("No encuentro nada", resp.texto())
            self.assertEqual(resp.fuentes(), [])

    def test_diagnostico_incluye_evento_y_scores(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = self._memoria(d)
            resp = responder("enlace covalente", k=2, ruta=ruta)
            diagnostico = resp.diagnostico()
            self.assertIn("evento:", diagnostico)
            self.assertIn("score", diagnostico)

    def test_pregunta_fuera_de_tema_no_inventa(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = self._memoria(d)  # química + filosofía
            resp = responder("quien gano el mundial de futbol", ruta=ruta)
            self.assertFalse(resp.hay_evidencia())
            self.assertIn("No encuentro nada", resp.texto())


if __name__ == "__main__":
    unittest.main()

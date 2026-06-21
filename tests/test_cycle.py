"""Pruebas del ciclo percepción → memoria → acción (cycle.ciclo)."""
import tempfile
import unittest
from pathlib import Path

from ampa.core.paths import Paths
from ampa.cycle import ciclo


class TestCiclo(unittest.TestCase):
    def _paths(self, d):
        return Paths(home=Path(d) / "home")

    def test_propuesta_no_persiste_nada(self):
        with tempfile.TemporaryDirectory() as d:
            paths = self._paths(d)
            res = ciclo("Revisar la definicion de enlace covalente", paths=paths)
            self.assertTrue(res.escritura.simulado)
            self.assertFalse(res.escritura.escrito)
            self.assertFalse(res.destino.exists())
            self.assertFalse(res.registrado)
            self.assertEqual(res.ingeridos, 0)

    def test_ejecutar_escribe_y_recuerda(self):
        with tempfile.TemporaryDirectory() as d:
            paths = self._paths(d)
            res = ciclo(
                "El enlace covalente es clave en la quimica organica",
                paths=paths,
                ejecutar=True,
            )
            self.assertTrue(res.escritura.escrito)
            self.assertTrue(res.destino.exists())
            contenido = res.destino.read_text(encoding="utf-8")
            self.assertIn("enlace covalente", contenido)
            self.assertIn("quimica", contenido)  # encabezado con el dominio
            self.assertTrue(res.registrado)  # química → guardar_en_memoria=True
            self.assertGreaterEqual(res.ingeridos, 1)

    def test_ejecutar_anexa_con_respaldo(self):
        with tempfile.TemporaryDirectory() as d:
            paths = self._paths(d)
            ciclo("Primera observacion sobre la oxidacion", paths=paths, ejecutar=True)
            res2 = ciclo(
                "Segunda observacion sobre la reduccion", paths=paths, ejecutar=True
            )
            contenido = res2.destino.read_text(encoding="utf-8")
            self.assertIn("Primera observacion", contenido)  # se anexa, no se pierde
            self.assertIn("Segunda observacion", contenido)
            self.assertIsNotNone(res2.escritura.respaldo)  # respaldo del estado previo

    def test_sin_registro_no_recuerda(self):
        with tempfile.TemporaryDirectory() as d:
            paths = self._paths(d)
            res = ciclo(
                "El enlace covalente comparte electrones",
                paths=paths,
                ejecutar=True,
                registrar=False,
            )
            self.assertTrue(res.escritura.escrito)
            self.assertFalse(res.registrado)
            self.assertEqual(res.ingeridos, 0)


if __name__ == "__main__":
    unittest.main()

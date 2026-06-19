"""Pruebas del Escriba seguro (scribe.writer)."""
import tempfile
import unittest
from pathlib import Path

from ampa.core.paths import Paths
from ampa.scribe import escribir, respaldos_de, restaurar


class TestScribe(unittest.TestCase):
    def _paths(self, d):
        # Aísla los respaldos en un home temporal.
        return Paths(home=Path(d) / "ampa_home")

    def test_crea_archivo_nuevo_sin_respaldo(self):
        with tempfile.TemporaryDirectory() as d:
            destino = Path(d) / "sub" / "nota.md"  # carpeta inexistente
            res = escribir(destino, "hola", paths=self._paths(d))
            self.assertTrue(res.escrito)
            self.assertIsNone(res.respaldo)
            self.assertEqual(destino.read_text(encoding="utf-8"), "hola")

    def test_sobrescribe_con_respaldo_previo(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._paths(d)
            destino = Path(d) / "nota.md"
            escribir(destino, "v1", paths=p)
            res = escribir(destino, "v2", paths=p)
            self.assertTrue(res.escrito)
            self.assertIsNotNone(res.respaldo)
            self.assertEqual(res.respaldo.read_text(encoding="utf-8"), "v1")
            self.assertEqual(destino.read_text(encoding="utf-8"), "v2")

    def test_simular_no_toca_disco(self):
        with tempfile.TemporaryDirectory() as d:
            destino = Path(d) / "nota.md"
            res = escribir(destino, "x", simular=True, paths=self._paths(d))
            self.assertTrue(res.simulado)
            self.assertFalse(res.escrito)
            self.assertFalse(destino.exists())

    def test_bloqueo_por_riesgo_alto(self):
        with tempfile.TemporaryDirectory() as d:
            destino = Path(d) / "nota.md"
            res = escribir(destino, "x", riesgo="alto", paths=self._paths(d))
            self.assertTrue(res.bloqueado)
            self.assertFalse(res.escrito)
            self.assertFalse(destino.exists())

    def test_forzar_supera_el_riesgo_alto(self):
        with tempfile.TemporaryDirectory() as d:
            destino = Path(d) / "nota.md"
            res = escribir(destino, "x", riesgo="alto", forzar=True, paths=self._paths(d))
            self.assertTrue(res.escrito)
            self.assertEqual(destino.read_text(encoding="utf-8"), "x")

    def test_sin_respaldo_no_crea_copia(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._paths(d)
            destino = Path(d) / "nota.md"
            escribir(destino, "v1", paths=p)
            res = escribir(destino, "v2", respaldar=False, paths=p)
            self.assertIsNone(res.respaldo)
            self.assertEqual(respaldos_de("nota.md", p), [])

    def test_restaurar_vuelve_al_contenido_anterior(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._paths(d)
            destino = Path(d) / "nota.md"
            escribir(destino, "bueno", paths=p)
            escribir(destino, "malo", paths=p)
            res = restaurar(destino, paths=p)
            self.assertTrue(res.escrito)
            self.assertEqual(destino.read_text(encoding="utf-8"), "bueno")

    def test_respaldos_orden_reciente_primero(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._paths(d)
            destino = Path(d) / "nota.md"
            escribir(destino, "1", paths=p)
            escribir(destino, "2", paths=p)  # respalda "1"
            escribir(destino, "3", paths=p)  # respalda "2"
            backups = respaldos_de("nota.md", p)
            self.assertEqual(len(backups), 2)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "2")
            self.assertEqual(backups[1].read_text(encoding="utf-8"), "1")


if __name__ == "__main__":
    unittest.main()

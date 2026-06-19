"""Pruebas del diario de eventos (journal)."""
import tempfile
import unittest
from pathlib import Path

from ampa.perception import journal, perceive
from ampa.perception.events import Evento


class TestJournal(unittest.TestCase):
    def test_registra_si_debe_guardarse(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "eventos.jsonl"
            ev = perceive("Describe la oxidación del hierro")  # química → guardar
            self.assertTrue(ev.guardar_en_memoria)
            self.assertTrue(journal.registrar(ev, ruta))
            registros = journal.leer(ruta)
            self.assertEqual(len(registros), 1)
            self.assertEqual(registros[0]["dominio_probable"], "quimica")
            self.assertIn("timestamp", registros[0])

    def test_omite_si_no_debe_guardarse(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "eventos.jsonl"
            ev = perceive("hola?")  # general breve → no guardar
            self.assertFalse(ev.guardar_en_memoria)
            self.assertFalse(journal.registrar(ev, ruta))
            self.assertEqual(journal.leer(ruta), [])

    def test_forzar_registra_igual(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "eventos.jsonl"
            ev = Evento(tipo="pregunta", dominio_probable="general")
            self.assertFalse(journal.registrar(ev, ruta))
            self.assertTrue(journal.registrar(ev, ruta, forzar=True))
            self.assertEqual(len(journal.leer(ruta)), 1)

    def test_varios_anexos(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "eventos.jsonl"
            for texto in ("enlace covalente", "epistemología de Kant"):
                journal.registrar(perceive(texto), ruta)
            self.assertEqual(len(journal.leer(ruta)), 2)

    def test_leer_inexistente_devuelve_vacio(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(journal.leer(Path(d) / "no_existe.jsonl"), [])


if __name__ == "__main__":
    unittest.main()

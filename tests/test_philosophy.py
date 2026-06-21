"""Pruebas del reconocimiento de filosofía (philosophy)."""
import tempfile
import unittest
from pathlib import Path

from ampa.philosophy import identificar, notebook


class TestFilosofia(unittest.TestCase):
    def test_filosofos_corrientes_y_conceptos(self):
        r = identificar(
            "Kant criticó el empirismo de Hume sobre el fenómeno y la metafísica."
        )
        filosofos = {f.nombre for f in r.filosofos}
        self.assertIn("Kant", filosofos)
        self.assertIn("Hume", filosofos)
        self.assertIn("empirismo", {c.nombre for c in r.corrientes})
        conceptos = {c.nombre for c in r.conceptos}
        self.assertIn("fenómeno", conceptos)
        self.assertIn("metafísica", conceptos)

    def test_metadatos_de_filosofo(self):
        r = identificar("Aristóteles fundó el realismo.")
        aristoteles = next(f for f in r.filosofos if f.nombre == "Aristóteles")
        self.assertEqual(aristoteles.epoca, "Antigua")
        self.assertEqual(aristoteles.categoria, "realismo")

    def test_marxismo_es_corriente_no_filosofo(self):
        r = identificar("El marxismo influyó en el siglo XX.")
        self.assertIn("marxismo", {c.nombre for c in r.corrientes})
        self.assertNotIn("Marx", {f.nombre for f in r.filosofos})

    def test_sin_falsos_positivos(self):
        r = identificar("El niño jugaba con la pelota en el jardín.")
        self.assertFalse(r.hay())

    def test_to_dict_estructura(self):
        r = identificar("Platón y el idealismo.")
        datos = r.to_dict()
        self.assertEqual({"filosofos", "corrientes", "conceptos"}, set(datos))
        self.assertEqual(datos["filosofos"][0]["nombre"], "Platón")


class TestCuaderno(unittest.TestCase):
    def test_agregar_con_terminos_explicitos_agrupa(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "pensamientos.jsonl"
            notebook.agregar("El ser es lo que persiste.", ["ser"], ruta=ruta)
            notebook.agregar("El Ser y el devenir.", ["Ser", "devenir"], ruta=ruta)
            dicc = notebook.diccionario(ruta)
            self.assertEqual(len(dicc["ser"]), 2)  # 'ser' y 'Ser' se agrupan
            self.assertIn("devenir", dicc)

    def test_terminos_detectados_automaticamente(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "pensamientos.jsonl"
            p = notebook.agregar("Pienso en la metafísica de Kant.", ruta=ruta)
            self.assertIn("metafísica", p.terminos)
            self.assertIn("Kant", p.terminos)

    def test_cuaderno_vacio(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "no.jsonl"
            self.assertEqual(notebook.leer(ruta), [])
            self.assertEqual(notebook.diccionario(ruta), {})


if __name__ == "__main__":
    unittest.main()

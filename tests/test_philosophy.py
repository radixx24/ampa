"""Pruebas del reconocimiento de filosofía (philosophy)."""
import unittest

from ampa.philosophy import identificar


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


if __name__ == "__main__":
    unittest.main()

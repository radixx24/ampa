"""Pruebas de la memoria documental (chunker, store, ingest, retriever)."""
import tempfile
import unittest
from pathlib import Path

from ampa.memory import cargar_fragmentos, ingerir, recuperar, trocear

QUIMICA = "El enlace covalente se forma cuando dos atomos comparten electrones de valencia."
FILOSOFIA = "La epistemologia de Kant distingue el fenomeno de la cosa en si misma."


class TestChunker(unittest.TestCase):
    def test_parrafos_cortos_se_conservan(self):
        self.assertEqual(trocear("Uno.\n\nDos.\n\nTres."), ["Uno.", "Dos.", "Tres."])

    def test_parrafo_largo_se_parte_con_solapamiento(self):
        texto = " ".join(str(i) for i in range(300))
        trozos = trocear(texto, max_palabras=100, solapamiento=20)
        self.assertGreater(len(trozos), 1)
        self.assertTrue(all(len(t.split()) <= 100 for t in trozos))


class TestIngestStore(unittest.TestCase):
    def test_ingesta_persiste_trocea_y_etiqueta_dominio(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "frag.jsonl"
            frags = ingerir(
                texto=f"{QUIMICA}\n\n{FILOSOFIA}", fuente="apuntes.md", ruta=ruta
            )
            self.assertEqual(len(frags), 2)
            self.assertEqual([f.indice for f in frags], [0, 1])
            self.assertEqual(frags[0].dominio, "quimica")
            self.assertEqual(frags[1].dominio, "filosofia")
            self.assertEqual(len(cargar_fragmentos(ruta)), 2)  # persistido


class TestRetriever(unittest.TestCase):
    def test_recupera_el_fragmento_relevante_con_cita(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "frag.jsonl"
            ingerir(texto=f"{QUIMICA}\n\n{FILOSOFIA}", fuente="apuntes.md", ruta=ruta)
            res = recuperar("que es el enlace covalente", k=3, ruta=ruta)
            self.assertTrue(res)
            self.assertIn("covalente", res[0].fragmento.texto)
            self.assertEqual(res[0].cita(), "[apuntes.md#0]")

    def test_sin_coincidencias_devuelve_vacio(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "frag.jsonl"
            ingerir(texto=QUIMICA, fuente="q.md", ruta=ruta)
            self.assertEqual(recuperar("zzzzz inexistente xyzzy", ruta=ruta), [])

    def test_k_limita_los_resultados(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "frag.jsonl"
            texto = "\n\n".join(f"atomo electron enlace numero {i}" for i in range(5))
            ingerir(texto=texto, fuente="multi.md", ruta=ruta, clasificar=False)
            self.assertEqual(len(recuperar("atomo enlace", k=2, ruta=ruta)), 2)


if __name__ == "__main__":
    unittest.main()

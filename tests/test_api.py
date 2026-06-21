"""Pruebas de la API (despacho puro, sin sockets)."""
import unittest

from ampa.api.server import manejar

ETANOL = {
    "nombre": "etanol",
    "atomos": ["C", "C", "O", "H", "H", "H", "H", "H", "H"],
    "enlaces": [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 4, 1], [0, 5, 1], [0, 6, 1], [1, 7, 1], [1, 8, 1]],
}


class TestApi(unittest.TestCase):
    def test_salud(self):
        status, cuerpo = manejar("GET", "/api/salud")
        self.assertEqual(status, 200)
        self.assertEqual(cuerpo["estado"], "ok")

    def test_tabla_periodica(self):
        status, cuerpo = manejar("GET", "/api/quimica/tabla")
        self.assertEqual(status, 200)
        self.assertEqual(len(cuerpo), 118)

    def test_identificar_quimica(self):
        status, cuerpo = manejar("POST", "/api/quimica/identificar", {"texto": "agua H2O"})
        self.assertEqual(status, 200)
        self.assertIn("H2O", {c["formula"] for c in cuerpo["compuestos"]})

    def test_analizar_molecula(self):
        status, cuerpo = manejar("POST", "/api/quimica/analizar", ETANOL)
        self.assertEqual(status, 200)
        self.assertEqual(cuerpo["formula"], "C2H6O")
        self.assertIn("alcohol", cuerpo["grupos_funcionales"])
        self.assertTrue(cuerpo["reacciones"])

    def test_identificar_filosofia(self):
        status, cuerpo = manejar("POST", "/api/filosofia/identificar", {"texto": "Kant y el idealismo"})
        self.assertEqual(status, 200)
        self.assertIn("Kant", {f["nombre"] for f in cuerpo["filosofos"]})

    def test_ruta_desconocida(self):
        status, _ = manejar("GET", "/api/no-existe")
        self.assertEqual(status, 404)

    def test_molecula_invalida_da_400(self):
        status, cuerpo = manejar(
            "POST", "/api/quimica/analizar", {"atomos": ["O", "H"], "enlaces": [[0, 9, 1]]}
        )
        self.assertEqual(status, 400)
        self.assertIn("error", cuerpo)


if __name__ == "__main__":
    unittest.main()

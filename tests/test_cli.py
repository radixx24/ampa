"""Pruebas de la CLI portable."""
import io
import unittest
from contextlib import redirect_stdout

from ampa.cli.main import main


class TestCli(unittest.TestCase):
    def _run(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(argv)
        return code, buf.getvalue()

    def test_version(self):
        code, out = self._run(["version"])
        self.assertEqual(code, 0)
        self.assertIn("AMPA", out)

    def test_info(self):
        code, out = self._run(["info"])
        self.assertEqual(code, 0)
        self.assertIn("Plataforma", out)
        self.assertIn("Rutas portables", out)

    def test_paths_lista(self):
        code, out = self._run(["paths"])
        self.assertEqual(code, 0)
        self.assertTrue(out.strip())

    def test_sin_comando_muestra_ayuda(self):
        code, out = self._run([])
        self.assertEqual(code, 0)
        self.assertIn("usage", out.lower())


if __name__ == "__main__":
    unittest.main()

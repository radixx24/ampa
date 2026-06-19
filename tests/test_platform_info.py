"""Pruebas del módulo de detección de plataforma.

Se ejecutan con biblioteca estándar:  ``python -m unittest discover -s tests -t .``
"""
import unittest

from ampa.core import platform_info as pi


class TestNormalizeSystem(unittest.TestCase):
    def test_windows_variantes(self):
        for raw in ("Windows", "windows", "WIN32", "Win"):
            self.assertEqual(pi.normalize_system(raw), pi.WINDOWS)

    def test_linux(self):
        self.assertEqual(pi.normalize_system("Linux"), pi.LINUX)

    def test_macos_variantes(self):
        for raw in ("Darwin", "darwin", "macOS"):
            self.assertEqual(pi.normalize_system(raw), pi.MACOS)

    def test_desconocido(self):
        self.assertEqual(pi.normalize_system("Plan9"), pi.UNKNOWN)


class TestCurrentSystem(unittest.TestCase):
    def test_flags_excluyentes(self):
        # Como mucho uno de los tres puede ser verdadero.
        flags = [pi.is_windows(), pi.is_linux(), pi.is_macos()]
        self.assertLessEqual(sum(flags), 1)

    def test_summary_tiene_claves(self):
        s = pi.summary()
        for clave in ("sistema", "arquitectura", "python", "ejecutable"):
            self.assertIn(clave, s)


if __name__ == "__main__":
    unittest.main()

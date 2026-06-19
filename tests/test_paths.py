"""Pruebas de rutas portables.

La clave: se inyectan ``system`` y ``env`` para simular Windows, macOS y Linux
**desde cualquier SO**, sin depender de dónde corran las pruebas.
"""
import tempfile
import unittest
from pathlib import Path

from ampa.core import paths as P


class TestResolveHome(unittest.TestCase):
    def test_override_ampa_home_manda_en_todos_los_so(self):
        env = {"AMPA_HOME": "/tmp/custom_ampa", "HOME": "/home/u"}
        for system in ("Windows", "Linux", "Darwin"):
            self.assertEqual(
                P.resolve_home(system=system, env=env),
                Path("/tmp/custom_ampa"),
            )

    def test_linux_con_xdg(self):
        env = {"HOME": "/home/u", "XDG_DATA_HOME": "/home/u/.xdg"}
        self.assertEqual(
            P.resolve_home(system="Linux", env=env),
            Path("/home/u/.xdg/ampa"),
        )

    def test_linux_por_defecto(self):
        env = {"HOME": "/home/u"}
        self.assertEqual(
            P.resolve_home(system="Linux", env=env),
            Path("/home/u/.local/share/ampa"),
        )

    def test_macos(self):
        env = {"HOME": "/Users/u"}
        self.assertEqual(
            P.resolve_home(system="Darwin", env=env),
            Path("/Users/u/Library/Application Support/AMPA"),
        )

    def test_windows_localappdata(self):
        env = {
            "USERPROFILE": r"C:\Users\u",
            "LOCALAPPDATA": r"C:\Users\u\AppData\Local",
        }
        self.assertEqual(
            P.resolve_home(system="Windows", env=env),
            Path(r"C:\Users\u\AppData\Local") / P.APP_NAME,
        )

    def test_windows_respaldo_userprofile(self):
        env = {"USERPROFILE": r"C:\Users\u"}
        self.assertEqual(
            P.resolve_home(system="Windows", env=env),
            Path(r"C:\Users\u") / P.APP_NAME,
        )


class TestPaths(unittest.TestCase):
    def test_subcarpetas_bajo_home(self):
        p = P.Paths(home=Path("/tmp/ampa_x"))
        self.assertEqual(p.data, Path("/tmp/ampa_x/data"))
        self.assertEqual(p.models, Path("/tmp/ampa_x/models"))
        self.assertEqual(p.memory, Path("/tmp/ampa_x/memory"))
        self.assertIn(p.backups, p.all())

    def test_create_es_idempotente(self):
        with tempfile.TemporaryDirectory() as d:
            p = P.Paths(home=Path(d) / "ampa").create()
            # Segunda llamada no debe fallar.
            p.create()
            for ruta in p.all():
                self.assertTrue(ruta.is_dir(), f"No se creó: {ruta}")


if __name__ == "__main__":
    unittest.main()

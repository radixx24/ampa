"""Empaqueta AMPA (web + API) en un ejecutable único con PyInstaller.

Requisitos: el frontend compilado (``frontend/dist``) y PyInstaller instalado.

    cd frontend && npm install && npm run build && cd ..
    pip install pyinstaller
    python packaging/build_exe.py

El ejecutable queda en ``dist_exe/``. No necesita Python ni Node para correr.
"""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def main() -> int:
    dist = RAIZ / "frontend" / "dist"
    if not dist.exists():
        print("Falta frontend/dist. Corre: cd frontend && npm install && npm run build")
        return 1
    try:
        import PyInstaller.__main__ as pyinstaller
    except ImportError:
        print("Falta PyInstaller. Instala con: pip install pyinstaller")
        return 1

    pyinstaller.run([
        str(RAIZ / "packaging" / "entry.py"),
        "--name", "ampakadabra",
        "--onefile",
        "--paths", str(RAIZ),
        "--add-data", f"{dist}{os.pathsep}frontend/dist",
        "--distpath", str(RAIZ / "dist_exe"),
        "--workpath", str(RAIZ / "build_exe"),
        "--specpath", str(RAIZ / "build_exe"),
        "--noconfirm",
    ])
    print(f"\nListo: {RAIZ / 'dist_exe'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

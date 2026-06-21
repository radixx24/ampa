"""Punto de entrada del ejecutable empaquetado (PyInstaller).

Arranca AMPA (web + API) y abre el navegador. El frontend compilado se incluye
dentro del paquete (ver ``build_exe.py``); el servidor lo localiza vía
``sys._MEIPASS`` (ADR 0015).
"""
import sys
import threading
import webbrowser

from ampa.api import servir


def main() -> int:
    puerto = 8000
    for i, arg in enumerate(sys.argv):
        if arg == "--puerto" and i + 1 < len(sys.argv):
            puerto = int(sys.argv[i + 1])
    url = f"http://127.0.0.1:{puerto}"
    print(f"\n  AMPA  -  abriendo {url}\n")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    servir(puerto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

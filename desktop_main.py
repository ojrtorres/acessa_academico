# desktop_main.py
import os
import threading
import time
import webbrowser
from waitress import serve

# Antes de importar a app, fixe o ambiente desktop
os.environ.setdefault("APP_ENV", "desktop")
os.environ.setdefault("FLASK_APP", "run.py")

from app import create_app  # noqa: E402

def run_server(app, port: int = 8765):
    # waitress é estável no Windows
    serve(app, host="127.0.0.1", port=port, threads=6)

def main():
    app = create_app()
    port = 8765
    t = threading.Thread(target=run_server, args=(app, port), daemon=True)
    t.start()

    time.sleep(0.8)  # pequeno atraso para subir
    webbrowser.open(f"http://127.0.0.1:{port}/auth/login", new=1)

    try:
        while t.is_alive():
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

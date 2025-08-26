﻿import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug = app.config.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)

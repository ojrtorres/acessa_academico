from __future__ import annotations

import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Extensões globais
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # rota de login


def _default_sqlite_uri() -> str:
    """
    Cria uma pasta 'AcessaAcademico' na home do usuário e usa um arquivo
    acessa.db como banco local. Usa barras '/' para evitar problemas de escape.
    """
    home = Path.home()
    data_dir = home / "AcessaAcademico"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "acessa.db"
    # Importante: trocar '\' por '/' na URI do SQLite no Windows
    return "sqlite:///" + str(db_path).replace("\\", "/")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # --- Config base (modo Desktop local) ---
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")
    app.config["BRAND_NAME"] = os.environ.get("BRAND_NAME", "Acessa Acadêmico")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", _default_sqlite_uri()
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Inicializa extensões ---
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import User  # importa modelos para o Alembic enxergar

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return User.query.get(int(user_id))

    login_manager.init_app(app)

    # --- Contexto para templates ---
    @app.context_processor
    def inject_globals():
        return {
            "BRAND_NAME": app.config.get("BRAND_NAME", "Acessa Acadêmico"),
        }

    @app.context_processor
    def inject_has_endpoint():
        # has_endpoint('blueprint.endpoint')
        def has_endpoint(endpoint: str) -> bool:
            return endpoint in app.view_functions

        return {"has_endpoint": has_endpoint}

    # --- Blueprints ---
    from .auth import auth_bp
    from .professor import professor_bp
    from .aluno import aluno_bp
    from .routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(professor_bp, url_prefix="/professor")
    app.register_blueprint(aluno_bp, url_prefix="/aluno")

    return app

# app/__init__.py
from __future__ import annotations
import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

def _fallback_sqlite_uri() -> str:
    base = Path.home() / "AcessaAcademico"
    base.mkdir(parents=True, exist_ok=True)
    return "sqlite:///" + str(base / "acessa.db").replace("\\", "/")

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # --- Config por APP_ENV usando CONFIG_MAP ---
    try:
        from .config import CONFIG_MAP  # type: ignore
        env = os.environ.get("APP_ENV", "desktop").lower()
        cfg = CONFIG_MAP.get(env) or CONFIG_MAP["desktop"]
        app.config.from_object(cfg)
    except Exception:
        # Fallback robusto (não quebra se faltar config.py)
        app.config.update(
            SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", _fallback_sqlite_uri()),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            BRAND_NAME="Acessa Acadêmico",
        )

    # --- Extensões ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- User loader ---
    from .models import User  # import local para evitar ciclo
    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # --- Blueprints ---
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    try:
        from .professor import professor_bp
        app.register_blueprint(professor_bp, url_prefix="/professor")
    except Exception:
        pass

    try:
        from .aluno import aluno_bp
        app.register_blueprint(aluno_bp, url_prefix="/aluno")
    except Exception:
        pass

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

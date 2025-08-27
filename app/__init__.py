# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from .config import get_config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(get_config())

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .auth import auth_bp
    from .professor import professor_bp
    from .aluno import aluno_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(professor_bp, url_prefix="/professor")
    app.register_blueprint(aluno_bp, url_prefix="/aluno")
    app.register_blueprint(main_bp)

    # Endpoints úteis no Desktop também
    @app.get("/health")
    def health():
        return {"ok": True}, 200

    @app.get("/version")
    def version():
        try:
            from importlib.metadata import version as v
            return {"app": "acessa_academico", "flask": v("Flask")}, 200
        except Exception:
            return {"app": "acessa_academico"}, 200

    return app

# necessário para Flask-Login: defina o user_loader se ainda não definiu em outro lugar:
from .models import User  # noqa: E402

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

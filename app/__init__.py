import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import CONFIG_MAP

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Carrega variáveis do .env (se existir)
    load_dotenv()

    env = os.getenv("APP_ENV", "development").lower()
    cfg_class = CONFIG_MAP.get(env, CONFIG_MAP["development"])

    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(cfg_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Importa modelos para o contexto de migração/autenticação
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .auth.routes import auth_bp
    from .professor.routes import professor_bp
    from .aluno.routes import aluno_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(professor_bp, url_prefix='/professor')
    app.register_blueprint(aluno_bp, url_prefix='/aluno')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'professor':
                return redirect(url_for('professor.dashboard'))
            if current_user.role == 'aluno':
                return redirect(url_for('aluno.dashboard'))
        return redirect(url_for('auth.login'))

    # Logging básico em produção
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        log_path = os.getenv("LOG_PATH", "app.log")
        fh = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
        fh.setLevel(logging.INFO)
        app.logger.addHandler(fh)

    return app

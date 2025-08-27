# app/config.py
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Diretório de dados por usuário (Windows/Mac/Linux)
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "AcessaAcademico")
os.makedirs(USER_DATA_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(USER_DATA_DIR, "acessa.db")

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SESSION_COOKIE_NAME = "acessa_session"
    WTF_CSRF_TIME_LIMIT = None

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"

class ProductionConfig(BaseConfig):
    DEBUG = False
    # Em produção (Render/Cloud), use DATABASE_URL (Postgres)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{os.path.join(BASE_DIR, 'prod.db')}"

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class DesktopConfig(BaseConfig):
    """Config para app empacotado no PC do usuário (sem rede)."""
    DEBUG = False
    # Banco local por usuário:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "desktop": DesktopConfig,
}

def get_config():
    env = os.environ.get("APP_ENV", "development").lower()
    return CONFIG_MAP.get(env, DevelopmentConfig)

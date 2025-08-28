# app/config.py
from __future__ import annotations
import os
from pathlib import Path

# Pasta padrão para o SQLite local (Desktop)
BASE_DIR = Path.home() / "AcessaAcademico"
BASE_DIR.mkdir(parents=True, exist_ok=True)  # garante que existe

def sqlite_uri(path: Path) -> str:
    # SQLAlchemy aceita "sqlite:///<PATH>" com barras normais
    return "sqlite:///" + str(path).replace("\\", "/")

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BRAND_NAME = "Acessa Acadêmico"

class DesktopConfig(BaseConfig):
    # Banco local do usuário (app desktop)
    SQLALCHEMY_DATABASE_URI = sqlite_uri(BASE_DIR / "acessa.db")

class DevelopmentConfig(BaseConfig):
    # Usa DATABASE_URL se existir, senão um SQLite dev
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        sqlite_uri(BASE_DIR / "acessa_dev.db"),
    )

class ProductionConfig(BaseConfig):
    # Produção exige DATABASE_URL (Postgres etc.)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")

CONFIG_MAP = {
    "desktop": DesktopConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

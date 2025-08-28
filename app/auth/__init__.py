# app/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

# importe as rotas **depois** de criar o blueprint
from . import routes  # noqa

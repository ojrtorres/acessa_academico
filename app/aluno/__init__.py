from flask import Blueprint

# O blueprint será criado de fato em routes.py
aluno_bp = Blueprint("aluno", __name__, template_folder="../templates/aluno")

# Importa as rotas para registrar no blueprint
from . import routes  # noqa

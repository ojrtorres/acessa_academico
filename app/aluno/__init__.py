from flask import Blueprint

aluno_bp = Blueprint("aluno", __name__, url_prefix="/aluno")

from . import routes  # noqa: F401,E402

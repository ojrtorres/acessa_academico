from flask import Blueprint
aluno_bp = Blueprint('aluno', __name__, template_folder='../templates/aluno')
from . import routes  # noqa

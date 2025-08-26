from flask import Blueprint
professor_bp = Blueprint('professor', __name__, template_folder='../templates/professor')
from . import routes  # noqa

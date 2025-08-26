from flask import render_template
from flask_login import login_required
from ..models import role_required
from . import professor_bp
@professor_bp.route('/dashboard')
@login_required
@role_required('professor')
def dashboard():
    # Conteúdo inicial; depois conectaremos aulas, tarefas, etc.
    stats = {
        'aulas_criadas': 0,
        'alunos_ativos': 0,
        'tarefas_pendentes': 0
    }
    return render_template('professor/dashboard.html', stats=stats)

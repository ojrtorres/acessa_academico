from __future__ import annotations

from flask import render_template
from flask_login import login_required, current_user

from app.models import role_required, AlunoProfile
from . import aluno_bp


@aluno_bp.route("/dashboard", methods=["GET"])
@login_required
@role_required("aluno")
def dashboard():
    perfil: AlunoProfile | None = getattr(current_user, "aluno_profile", None)
    resumo = {
        "aulas_em_andamento": 0,
        "tarefas_pendentes": 0,
        "avisos": 0,
        "curso": perfil.curso if perfil else None,
        "turma": perfil.turma if perfil else None,
    }
    return render_template("aluno/dashboard.html", resumo=resumo)


@aluno_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@role_required("aluno")
def perfil():
    perfil: AlunoProfile | None = getattr(current_user, "aluno_profile", None)
    return render_template("aluno/perfil.html", perfil=perfil)

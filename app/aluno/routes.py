from __future__ import annotations
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import aluno_bp
from app import db
from app.models import AlunoProfile

def _ensure_aluno_profile():
    """Garante que o aluno logado tem um AlunoProfile; cria se não existir."""
    perfil = current_user.aluno_profile
    if not perfil:
        perfil = AlunoProfile(user_id=current_user.id)
        db.session.add(perfil)
        db.session.commit()
    return perfil

@aluno_bp.get("/dashboard")
@login_required
def dashboard():
    # Proteção por papel
    if current_user.role != "aluno":
        flash("Acesso permitido apenas a alunos.", "warning")
        return redirect(url_for("main.index"))

    # Resumo mínimo para o template (placeholders seguros)
    resumo = {
        "aulas_em_andamento": 0,
        "tarefas_pendentes": 0,
        "materiais_novos": 0,
        "mensagens": 0,
        "progresso_percent": 0,
        "proximas_avaliacoes": [],  # lista de dicionários se quiser
    }

    return render_template("aluno/dashboard.html", resumo=resumo)

@aluno_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    if current_user.role != "aluno":
        flash("Acesso permitido apenas a alunos.", "warning")
        return redirect(url_for("main.index"))

    perfil = _ensure_aluno_profile()

    if request.method == "POST":
        perfil.curso = request.form.get("curso") or perfil.curso
        perfil.turma = request.form.get("turma") or perfil.turma
        perfil.deficiencia = request.form.get("deficiencia") or perfil.deficiencia
        perfil.cid_code = request.form.get("cid_code") or perfil.cid_code
        perfil.observacoes = request.form.get("observacoes") or perfil.observacoes
        db.session.commit()
        flash("Perfil atualizado com sucesso.", "success")
        return redirect(url_for("aluno.perfil"))

    return render_template("aluno/perfil.html", perfil=perfil)

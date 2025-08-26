from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import role_required, AlunoProfile
from .. import db
from . import aluno_bp
from .forms import AlunoPerfilForm

@aluno_bp.route('/dashboard')
@login_required
@role_required('aluno')
def dashboard():
    resumo = {
        'aulas_em_andamento': 0,
        'tarefas_pendentes': 0,
    }
    return render_template('aluno/dashboard.html', resumo=resumo)

@aluno_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@role_required('aluno')
def perfil():
    # Garante que o aluno tenha um perfil vinculado
    profile = current_user.aluno_profile
    if profile is None:
        profile = AlunoProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

    form = AlunoPerfilForm(obj=profile)

    if form.validate_on_submit():
        profile.curso = form.curso.data or None
        profile.turma = form.turma.data or None
        profile.deficiencia = form.deficiencia.data or None
        profile.cid_code = form.cid_code.data or None
        profile.observacoes = form.observacoes.data or None

        db.session.commit()
        flash('Perfil atualizado com sucesso.', 'success')
        return redirect(url_for('aluno.perfil'))

    return render_template('aluno/perfil.html', form=form)

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User, AlunoProfile, ProfessorProfile
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        # Redireciona conforme perfil
        return redirect(url_for('professor.dashboard' if current_user.role=='professor' else 'aluno.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('professor.dashboard' if user.role=='professor' else 'aluno.dashboard'))
        flash('Credenciais inválidas. Verifique e tente novamente.', 'danger')
    return render_template('auth/login.html', form=form)
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('professor.dashboard' if current_user.role=='professor' else 'aluno.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'warning')
            return redirect(url_for('auth.register'))
        user = User(email=email, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # para obter user.id
        if user.role == 'aluno':
            db.session.add(AlunoProfile(user_id=user.id))
        else:
            db.session.add(ProfessorProfile(user_id=user.id))
        db.session.commit()
        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

from __future__ import annotations

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models import User, AlunoProfile, ProfessorProfile
from . import auth_bp
from .forms import LoginForm, RegisterForm


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # Já logado: manda para o dashboard conforme o papel
        if current_user.role == "professor":
            return redirect(url_for("professor.dashboard"))
        return redirect(url_for("aluno.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user: User | None = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get("next")
            try:
                if user.role == "professor":
                    return redirect(next_url or url_for("professor.dashboard"))
                else:
                    return redirect(next_url or url_for("aluno.dashboard"))
            except Exception:
                # Se por algum motivo o endpoint não existir, cai no index
                return redirect(url_for("main.index"))
        flash("Credenciais inválidas.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user.role == "professor":
            return redirect(url_for("professor.dashboard"))
        return redirect(url_for("aluno.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        role = form.role.data  # 'aluno' ou 'professor'
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "warning")
            return render_template("auth/register.html", form=form)

        user = User(email=email, role=role)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # obtém user.id

        if role == "aluno":
            db.session.add(AlunoProfile(user_id=user.id))
        else:
            db.session.add(ProfessorProfile(user_id=user.id))

        db.session.commit()
        flash("Conta criada com sucesso. Faça login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sessão.", "success")
    return redirect(url_for("auth.login"))

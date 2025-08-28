# app/auth/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from . import auth_bp
from .forms import LoginForm, RegisterForm
from app import db
from app.models import User, AlunoProfile, ProfessorProfile


def _norm_email(v: str) -> str:
    return (v or "").strip().lower()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Já logado -> manda pro dashboard correto
    if current_user.is_authenticated:
        if current_user.role == "professor":
            return redirect(url_for("professor.dashboard"))
        if current_user.role == "aluno":
            return redirect(url_for("aluno.dashboard"))
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = _norm_email(form.email.data)
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            nxt = request.args.get("next")
            return redirect(nxt or url_for("professor.dashboard" if user.role == "professor" else "aluno.dashboard"))
        flash("E-mail ou senha inválidos.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Já logado -> manda pro dashboard
    if current_user.is_authenticated:
        if current_user.role == "professor":
            return redirect(url_for("professor.dashboard"))
        if current_user.role == "aluno":
            return redirect(url_for("aluno.dashboard"))
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = _norm_email(form.email.data)
        role = form.role.data

        try:
            # evita duplicata
            if User.query.filter_by(email=email).first():
                flash("Já existe uma conta com este e-mail.", "warning")
                return redirect(url_for("auth.register"))

            user = User(email=email, role=role)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()  # garante user.id antes do commit

            # cria perfil one-to-one conforme a role
            if role == "aluno":
                db.session.add(AlunoProfile(user_id=user.id))
            elif role == "professor":
                db.session.add(ProfessorProfile(user_id=user.id))

            db.session.commit()
            flash("Conta criada com sucesso. Faça login.", "success")
            return redirect(url_for("auth.login"))

        except IntegrityError:
            db.session.rollback()
            flash("E-mail já cadastrado.", "warning")
            return redirect(url_for("auth.register"))
        except Exception:
            db.session.rollback()
            flash("Erro ao criar conta. Tente novamente.", "danger")
            return redirect(url_for("auth.register"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("auth.login"))

# app/routes.py
from flask import Blueprint, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    if current_user.is_authenticated:
        if current_user.role == "professor":
            return redirect(url_for("professor.dashboard"))
        if current_user.role == "aluno":
            return redirect(url_for("aluno.dashboard"))
    return redirect(url_for("auth.login"))

@main_bp.get("/dashboard")
def dashboard_fallback():
    return redirect(url_for("main.index"))

@main_bp.get("/health")
def health():
    return {"status": "ok"}

@main_bp.get("/version")
def version():
    return {"name": "Acessa Acadêmico", "version": "0.1.0"}

# app/models.py
from __future__ import annotations

from datetime import datetime
from functools import wraps

from flask import abort
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

__all__ = ["User", "AlunoProfile", "ProfessorProfile", "role_required"]

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="aluno")  # 'professor' ou 'aluno'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Perfis (one-to-one opcionais)
    aluno_profile = db.relationship("AlunoProfile", uselist=False, back_populates="user")
    professor_profile = db.relationship("ProfessorProfile", uselist=False, back_populates="user")

    # Helpers de senha
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.id} {self.email} ({self.role})>"

class AlunoProfile(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    curso = db.Column(db.String(120))
    turma = db.Column(db.String(120))

    # Dados sensíveis (privacidade!)
    deficiencia = db.Column(db.String(120))   # ex: visual, auditiva, motora...
    cid_code = db.Column(db.String(20))       # CID correspondente
    observacoes = db.Column(db.Text)

    user = db.relationship("User", back_populates="aluno_profile")

    def __repr__(self) -> str:
        return f"<AlunoProfile {self.id} user={self.user_id}>"

class ProfessorProfile(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    departamento = db.Column(db.String(120))

    user = db.relationship("User", back_populates="professor_profile")

    def __repr__(self) -> str:
        return f"<ProfessorProfile {self.id} user={self.user_id}>"

# Decorator simples de controle por papel
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from flask_login import current_user
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)  # proibido
            return f(*args, **kwargs)
        return decorated
    return wrapper

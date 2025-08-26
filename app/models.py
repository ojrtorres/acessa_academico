from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort
from . import db
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role        = db.Column(db.String(50), nullable=False, default='aluno')  # 'professor' ou 'aluno'
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    # Perfis (one-to-one opcionais)
    aluno_profile     = db.relationship('AlunoProfile', uselist=False, back_populates='user')
    professor_profile = db.relationship('ProfessorProfile', uselist=False, back_populates='user')
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
class AlunoProfile(db.Model):
    __tablename__ = 'alunos'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    curso       = db.Column(db.String(120))
    turma       = db.Column(db.String(120))
    # Dados sensíveis (privacidade!)
    deficiencia = db.Column(db.String(120))   # ex: visual, auditiva, motora...
    cid_code    = db.Column(db.String(20))    # CID correspondente
    observacoes = db.Column(db.Text)
    user        = db.relationship('User', back_populates='aluno_profile')
class ProfessorProfile(db.Model):
    __tablename__ = 'professores'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    departamento= db.Column(db.String(120))
    user        = db.relationship('User', back_populates='professor_profile')
# Decorator simples de controle por papel
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from flask_login import current_user
            if not current_user.is_authenticated or current_user.role not in roles:
                # 403 para proibido, evita vazar informação
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return wrapper

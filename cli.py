import click
from flask import current_app
from . import db
from .models import User, AlunoProfile, ProfessorProfile

def register_cli(app):
    @app.cli.group("user")
    def user_group():
        """Comandos para gerenciar usuários (criar, listar)."""
        pass

    @user_group.command("create")
    @click.option("--email", prompt=True, help="E-mail do usuário")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Senha do usuário")
    @click.option("--role", type=click.Choice(["aluno", "professor"]), prompt=True, help="Papel do usuário")
    @click.option("--curso", default=None, help="(Aluno) Curso")
    @click.option("--turma", default=None, help="(Aluno) Turma")
    @click.option("--departamento", default=None, help="(Professor) Departamento")
    def create_user(email, password, role, curso, turma, departamento):
        """Cria um usuário com papel aluno/professor e perfil correspondente."""
        with app.app_context():
            email = email.strip().lower()
            if User.query.filter_by(email=email).first():
                click.secho(f"[ERRO] E-mail já cadastrado: {email}", fg="red")
                return

            u = User(email=email, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.flush()  # garante u.id

            if role == "aluno":
                db.session.add(AlunoProfile(user_id=u.id, curso=curso, turma=turma))
            else:
                db.session.add(ProfessorProfile(user_id=u.id, departamento=departamento))

            db.session.commit()
            click.secho(f"[OK] Usuário criado: {email} ({role})", fg="green")

    @user_group.command("list")
    def list_users():
        """Lista usuários com seu papel."""
        with app.app_context():
            users = User.query.order_by(User.id.asc()).all()
            if not users:
                click.echo("Nenhum usuário encontrado.")
                return
            width = 30
            click.echo(f"{'ID':<4} {'EMAIL':<{width}} ROLE")
            click.echo("-" * (4 + 1 + width + 1 + 10))
            for u in users:
                click.echo(f"{u.id:<4} {u.email:<{width}} {u.role}")

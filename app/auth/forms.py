from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')
class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=64)])
    confirm  = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    role     = SelectField('Perfil', choices=[('aluno','Aluno'), ('professor','Professor')], validators=[DataRequired()])
    submit   = SubmitField('Criar Conta')

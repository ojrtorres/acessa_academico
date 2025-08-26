from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Length, Optional

class AlunoPerfilForm(FlaskForm):
    curso = StringField('Curso', validators=[Optional(), Length(max=120)])
    turma = StringField('Turma', validators=[Optional(), Length(max=120)])
    deficiencia = SelectField(
        'Deficiência',
        choices=[
            ('', 'Selecione...'),
            ('visual', 'Visual'),
            ('auditiva', 'Auditiva'),
            ('motora', 'Motora'),
            ('intelectual', 'Intelectual'),
            ('multipla', 'Múltipla'),
            ('outra', 'Outra')
        ],
        validators=[Optional()]
    )
    cid_code = StringField('CID', validators=[Optional(), Length(max=20)])
    observacoes = TextAreaField('Observações pedagógicas', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Salvar alterações')

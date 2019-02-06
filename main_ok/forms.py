from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, FieldList, SubmitField, SelectField
from wtforms.validators import DataRequired
from main_ok.models import User, Vote


class UserForm(FlaskForm):
    name = TextField('Имя', validators=[DataRequired()])
    login = TextField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class VoteForm(FlaskForm):
    title = TextField('Заголовок', validators=[DataRequired()])
    description = TextField('Текс вопроса', validators=[DataRequired()])
    # author_id = TextField('Автор', validators=[DataRequired()])
    answers = FieldList(TextField(validators=[DataRequired()]), label='Варианты ответа', min_entries=2)
    radio_checkbox = SelectField('Количество ответов', choices=[(0, 'несколько ответов'), (1, 'один ответ')])
    add = SubmitField(label='Добавить ответ')
    dela = SubmitField(label='Удалить ответ')


class LoginForm(FlaskForm):
    login = TextField('Логин')
    password = PasswordField('Пароль')
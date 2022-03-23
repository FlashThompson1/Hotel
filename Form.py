from flask_wtf import FlaskForm
from Database import User
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional


class SignIn(FlaskForm):
    email = EmailField('Адресс электронный почти ', validators=[DataRequired(), Email()])
    psw = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ManSign(FlaskForm):
    email = EmailField('Адресс электронный почти', validators=[DataRequired(), Email()])
    psw = PasswordField('Пароль', validators=[DataRequired()])
    extrapass = PasswordField('Введите ваш ID код Мэнеджера')
    submit = SubmitField('Войти')


class Registration(FlaskForm):
    firname = StringField('Имя')
    secname = StringField('Фамилия')
    email = EmailField('Адресс электронный почти', validators=[DataRequired(), Email()])
    psw = PasswordField('Пароль', validators=[DataRequired()])
    country = StringField('Страна')
    city = StringField('Город')
    passdata = FileField('Пасспортные данные', validators=[Optional()])
    submit = SubmitField('Авторизоватся')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Адресс электронный почты уже зарегистривован')



class ManRegistration(FlaskForm):
    firname = StringField('Имя')
    secname = StringField('Фамилия')
    email = EmailField('Адресс электронный почти')
    psw = PasswordField('Пароль')
    country = StringField('Страна')
    city = StringField('Город')
    extrapass = PasswordField('Введите ID код Мэнеджера ')
    submit = SubmitField('Авторизоватся')

class InfoUpdate(FlaskForm):
    firname = StringField('Имя')
    secname = StringField('Фамилия')
    email = EmailField('E-mail')
    country = StringField('Страна')
    city = StringField('Город')
    submit = SubmitField('Обновить Данные')



class Booking(FlaskForm):
    room = StringField('Введите номер которого хотите бронировать :', validators=[DataRequired()])
    bookingfrom = DateField('Забронировать с:', format='%Y-%m-%d', validators=[DataRequired()])
    bookingto = DateField('Забронировать до:', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Забранировать')


class PasswordRec(FlaskForm):
    email = EmailField('Введите вашу электронную почту: ', validators=[DataRequired()])
    submit = SubmitField('Отправка')

class NewPasswordRec(FlaskForm):
    email = EmailField('Введите вашу электронную почту: ', validators=[DataRequired()])
    psw = PasswordField('Введите ваш новый пароль: ', validators=[DataRequired()])
    submit = SubmitField('Сохранить данные ')





from application.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class SignupForm(FlaskForm):
    name = StringField('ニックネーム',
                       validators=[DataRequired('必須です'),
                                   Length(max=80, message='80桁までです')])
    email = StringField('メールアドレス',
                        validators=[DataRequired('必須です'),
                                    Length(max=120, message='120桁までです'),
                                    Email('メールアドレスの形式が違います')])
    password = PasswordField('パスワード',
                             validators=[DataRequired('必須です'),
                                         Length(max=30, message='30桁までです'),
                                         EqualTo('confirm', message='パスワードが再入力と一致していません')])
    confirm = PasswordField('パスワード（再入力）',
                            validators=[DataRequired('必須です')])

    def validate_name(self, field):
        if User.query.filter(User.name == field.data).count() > 0:
            raise ValidationError('すでに使われています')

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).count() > 0:
            raise ValidationError('すでに使われています')

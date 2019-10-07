from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('メールアドレス',
                        validators=[DataRequired('必須です'),
                                    Length(max=120, message='120桁までです'),
                                    Email('メールアドレスの形式が違います')])
    password = PasswordField('パスワード',
                             validators=[DataRequired('必須です'),
                                         Length(max=30, message='30桁までです')])

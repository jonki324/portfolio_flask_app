from application.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp


class SignupForm(FlaskForm):
    user_id = StringField('ユーザーID',
                          validators=[DataRequired('必須です'),
                                      Length(max=80, message='80桁までです'),
                                      Regexp('^[0-9A-Za-z]+$', message='半角英数字のみです')])
    email = StringField('メールアドレス',
                        validators=[DataRequired('必須です'),
                                    Length(max=120, message='120桁までです'),
                                    Email('メールアドレスの形式が違います')])
    password = PasswordField('パスワード',
                             validators=[DataRequired('必須です'),
                                         Length(max=30, message='30桁までです'),
                                         EqualTo('confirm', message='パスワードが再入力と一致していません'),
                                         Regexp('^[0-9A-Za-z]+$', message='半角英数字のみです')])
    confirm = PasswordField('パスワード（再入力）',
                            validators=[DataRequired('必須です')])

    def validate_user_id(self, field):
        if User.query.filter(User.user_id == field.data).count() > 0:
            raise ValidationError('すでに使われています')

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).count() > 0:
            raise ValidationError('すでに使われています')

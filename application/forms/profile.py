from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, TextAreaField, BooleanField
from wtforms.validators import Length


class ProfileForm(FlaskForm):
    nickname = StringField('ニックネーム',
                           validators=[Length(max=80, message='80桁までです')])
    comment = TextAreaField('コメント',
                            validators=[Length(max=200, message='200桁までです')])
    icon = FileField('アイコン',
                     validators=[FileAllowed(['jpg', 'jpeg'], message='jpgファイルのみです')])
    icon_del = BooleanField('現在のアイコンを削除する')

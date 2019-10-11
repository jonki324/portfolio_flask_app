from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, TextAreaField, BooleanField
from wtforms.validators import Length

images = UploadSet('images', IMAGES)


class ProfileForm(FlaskForm):
    nickname = StringField('ニックネーム',
                           validators=[Length(max=80, message='80桁までです')])
    comment = TextAreaField('コメント',
                            validators=[Length(max=200, message='200桁までです')])
    icon = FileField('アイコン',
                     validators=[FileAllowed(['jpg'], message='jpgファイルのみです')])
    icon_del = BooleanField('アイコンを削除する')

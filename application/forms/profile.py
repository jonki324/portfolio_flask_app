from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, TextAreaField
from wtforms.validators import Length

images = UploadSet('images', IMAGES)


class ProfileForm(FlaskForm):
    nickname = StringField('ニックネーム',
                           validators=[Length(max=80, message='80桁までです')])
    comment = TextAreaField('コメント',
                            validators=[Length(max=200, message='200桁までです')])
    icon = FileField('アイコン',
                     validators=[FileAllowed(images, message='イメージファイルのみです')])

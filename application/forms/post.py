from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length

images = UploadSet('images', IMAGES)


class PostForm(FlaskForm):
    title = StringField('タイトル',
                        validators=[DataRequired('必須です'),
                                    Length(max=100, message='100桁までです')])
    body = TextAreaField('コメント',
                         validators=[DataRequired('必須です'),
                                     Length(max=200, message='200桁までです')])
    image = FileField('ピクチャ',
                      validators=[FileAllowed(['jpg'], message='jpgファイルのみです')])
    is_img_saved = HiddenField()

    def validate_image(self, field):
        if not field.data:
            if not self.is_img_saved.data:
                raise ValidationError('必須です')

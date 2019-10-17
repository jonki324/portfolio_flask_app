from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


class IndexForm(FlaskForm):
    keyword = StringField('キーワード',
                          validators=[Length(max=200, message='200桁までです')])

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TryLetter(FlaskForm):
    letter = StringField('letter', validators=[DataRequired(),Length(min=1, max=1)])
    submit = SubmitField('Poiskusi')
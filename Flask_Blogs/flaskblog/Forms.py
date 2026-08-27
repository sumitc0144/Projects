from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from wtforms import BooleanField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length,EqualTo, ValidationError
from flaskblog.models import User

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    

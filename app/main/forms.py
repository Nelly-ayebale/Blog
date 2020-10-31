from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField('Subject of Blog', validators=[Required()])
    blog = TextAreaField('Enter Your Opinion', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us something about you', validators=[Required()])
    submit = SubmitField('Submit')
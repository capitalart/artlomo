from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

class AnalysisForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=140)])
    description = TextAreaField('Description')
    tags = StringField('SEO Tags')
    materials = StringField('Materials Used')
    seo_filename = StringField('SEO Filename')
    location = TextAreaField('Location / Inspiration')
    sentiment = TextAreaField('General Info / Sentiment')
    original_prompt = TextAreaField('Original Generation Prompt')
    action = HiddenField('Action', default='save')

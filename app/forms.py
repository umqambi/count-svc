from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class SiteChekForm(FlaskForm):
    site = StringField("Site: ", validators=[URL()])
    submit = SubmitField("Chek")
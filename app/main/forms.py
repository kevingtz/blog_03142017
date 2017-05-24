# HERE WE GONNA DEFINE OUR FORMS IN ORDER TO GET DATA FOR OUR USERS

# FIRST AT ALL WE NEED TO IMPORT WTF IN ORDER TO UDE FORMS AND ALSO WE GONNA NEED DATA VALIDATORS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# WE CREATE A CLASS IN ORDER TO CREATE OUR FIRST FORM

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

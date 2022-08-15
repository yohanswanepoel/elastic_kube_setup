from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, InputRequired
import utils

class ConfigForm(FlaskForm):
    kubectl_command = SelectField("Kubectl command: ", coerce=str, validators=[InputRequired()])
    local_cluster = SelectField("Local cluster type: ", coerce=str, validators=[InputRequired()])
    submit = SubmitField("Submit")

class InstallOperatorForm(FlaskForm):
    operator_version = SelectField("Operator Version: ", coerce=str, validators=[InputRequired()])
    submit = SubmitField("Submit")

class DeployStackForm(FlaskForm):
    namespace = StringField("Namespace: ", validators=[DataRequired()])
    version = SelectField("Version: ", coerce=str, validators=[InputRequired()])
    submit = SubmitField("Submit")

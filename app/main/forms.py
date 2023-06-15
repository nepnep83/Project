from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput
from wtforms.fields import RadioField, SubmitField, StringField
from wtforms.validators import InputRequired, Regexp, Length, Optional


class BankDetailsForm(FlaskForm):
    job_title = StringField(
        "Job title",
        widget=GovTextInput(),
        validators=[InputRequired(message="Enter your job title")],
    )
    sort_code = StringField(
        "Sort code",
        widget=GovTextInput(),
        validators=[
            InputRequired(message="Enter a sort code"),
            Regexp(regex=r"\d{6}", message="Enter a valid sort code like 309430"),
        ],
        description="Must be 6 digits long",
    )
    account_number = StringField(
        "Account number",
        widget=GovTextInput(),
        validators=[
            InputRequired(message="Enter an account number"),
            Regexp(regex=r"\d{6,8}", message="Enter a valid account number like 00733445"),
            Length(min=6, max=8, message="Account number must be between 6 and 8 digits"),
        ],
        description="Must be between 6 and 8 digits long",
    )
    roll_number = StringField(
        "Building society roll number (if you have one)",
        widget=GovTextInput(),
        validators=[
            Optional(),
            Length(
                min=1,
                max=18,
                message="Building society roll number must be between 1 and 18 characters",
            ),
            Regexp(
                regex=r"[a-zA-Z0-9- /.]*$",
                message="Building society roll number must only include letters a to z, numbers, hyphens, spaces, forward slashes and full stops",
            ),
        ],
        description="You can find it on your card, statement or passbook",
    )
    submit = SubmitField("Continue", widget=GovSubmitInput())

class CookiesForm(FlaskForm):
    functional = RadioField(
        "Do you want to accept functional cookies?",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Select yes if you want to accept functional cookies")],
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    analytics = RadioField(
        "Do you want to accept analytics cookies?",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Select yes if you want to accept analytics cookies")],
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    save = SubmitField("Save cookie settings", widget=GovSubmitInput())

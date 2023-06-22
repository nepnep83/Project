from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput
from wtforms.fields import RadioField, SubmitField, StringField
from wtforms.validators import InputRequired, Regexp, Length, Optional
from app.main.custom_validators import RequiredIf

class JobTitle(FlaskForm):
    radio = RadioField(
        "Have you worked previously?",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Select one option")],
        choices=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        description="Select one option.",
    )

    job_title = StringField(
        "Job title",
        widget=GovTextInput(),
        validators=[
                    RequiredIf(
                        "radio",
                        "yes",
                    ),
                    Regexp(
                        regex=r"[a-zA-Z ^!@£$%&()€#_=+-≠\[\\\]{}\"';\\\:|?,./âêîôûŵŷÂÊÎÔÛŴŶ]*$",
                        message="Inputs must only contain alphabetical and selected special characters",
                    ),
                    ]
    )
    submit = SubmitField("Continue", widget=GovSubmitInput())


class PrefJob(FlaskForm):
    radio = RadioField(
        "How would you prefer to be contacted?",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Select one option")],
        choices=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        description="Select one option.",
    )
    pref_job = StringField(
        "Job",
        widget=GovTextInput(),
        validators=[Length(max=100, message="Input must not be more than 100 characters"),
                    RequiredIf(
                        "radio",
                        "yes",
                    ),
                    Regexp(
                        regex=r"[a-zA-Z ^!@£$%&()€#_=+-≠\[\\\]{}\"';\\\:|?,./âêîôûŵŷÂÊÎÔÛŴŶ]*$",
                        message="Inputs must only contain alphabetical and selected special characters",
                    ),
                    ]
    )
    submit = SubmitField("Continue", widget=GovSubmitInput())


class Postcode(FlaskForm):
    postcode = StringField(
        "postcode",
        widget=GovTextInput(),
        validators=[Length(min=1, max=8, message="Postcode must be at least 1 character long"),
                    Regexp(
                        regex=r"[a-zA-Z 0-9]*$",
                        message="Inputs must only contain alphanumeric characters",
                    ),
                    ]
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

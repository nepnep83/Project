import uuid

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import csv
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException
from app.main import bp
from app.main.forms import CookiesForm, BankDetailsForm

user_info = "user_info"
user_account = "user_account"


@bp.route("/", methods=["GET", "POST"])
def index():
    form = BankDetailsForm()
    if form.validate_on_submit():
        store_data(form.job_title)
        return redirect(url_for("main.preferred"))
    return render_template("index.html", form=form)


@bp.route("/preferred")
def preferred():
    form = BankDetailsForm()
    if form.validate_on_submit():
        store_data(form.pref_job)
        return redirect(url_for("main.postcode"))
    return render_template("preferred.html")


@bp.route("/postcode")
def postcode():
    form = BankDetailsForm()
    if form.validate_on_submit():
        store_data(form.postcode)
        return redirect(url_for("main.summary"))
    return render_template("postcode.html")


@bp.route("/summary")
def summary():
    return render_template("summary.html")


@bp.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")


@bp.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookiesForm()
    # Default cookies policy to reject all categories of cookie
    cookies_policy = {"functional": "no", "analytics": "no"}

    if form.validate_on_submit():
        # Update cookies policy consent from form data
        cookies_policy["functional"] = form.functional.data
        cookies_policy["analytics"] = form.analytics.data

        # Create flash message confirmation before rendering template
        flash("You’ve set your cookie preferences.", "success")

        # Create the response so we can set the cookie before returning
        response = make_response(render_template("cookies.html", form=form))

        # Set cookies policy for one year
        response.set_cookie("cookies_policy", json.dumps(cookies_policy), max_age=31557600)
        return response
    elif request.method == "GET":
        if request.cookies.get("cookies_policy"):
            # Set cookie consent radios to current consent
            cookies_policy = json.loads(request.cookies.get("cookies_policy"))
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
        else:
            # If conset not previously set, use default "no" policy
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
    return render_template("cookies.html", form=form)


def store_data(info):
    ident = str(uuid.uuid4())
    session['id'] = ident
    print(session['id'])



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()

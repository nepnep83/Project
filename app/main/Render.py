import uuid

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import csv
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException
from app.main import bp
from app.main.forms import CookiesForm, JobTitle, PrefJob, Postcode

from Backend import recommend_jobs, job_vacancies

user_info = "user_info"
user_account = "user_account"


@bp.route("/", methods=["GET", "POST"])
def index():
    form = JobTitle()
    if form.validate_on_submit():
        session['job_title'] = form.job_title.data
        session['job_title_2'] = form.job_title_2.data
        return redirect(url_for("main.preferred"))
    return render_template("index.html", form=form)


@bp.route("/preferred", methods=["GET", "POST"])
def preferred():
    form = PrefJob()
    if form.validate_on_submit():
        session['pref_job'] = form.pref_job.data
        return redirect(url_for("main.postcode"))
    return render_template("preferred.html", form=form)


@bp.route("/postcode", methods=["GET", "POST"])
def postcode():
    form = Postcode()
    if form.validate_on_submit():
        session['postcode'] = form.postcode.data
        return redirect(url_for("main.summary"))
    return render_template("postcode.html", form=form)


@bp.route("/summary", methods=["GET", "POST"])
def summary():

    return render_template("summary.html", job_title=session['job_title'], pref_job=session['pref_job'],
                           postcode=session['postcode'])


@bp.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    jobs = [session['job_title'], session['job_title_2']]
    interest = [session['pref_job']]
    postcode = session['postcode']
    data_1, data_2 = job_vacancies.run(jobs, interest, 10, postcode, 5)
    recommend_job_1 = data_1[0]
    recommend_job_2 = data_1[1]
    recommend_job_3 = data_1[2]
    recommend_job_4 = data_1[3]
    recommend_job_5 = data_1[4]
    for i in range(1):
        session['preferred_job_' + str(i + 1)] = {"link": data_2[i]["link"],
                                                  "summary": data_2[i]["summary"],
                                                  "title": data_2[i]["title"]}
    return render_template("recommendation.html",
                           desc1=recommend_job_1['summary'],
                           job1=recommend_job_1['title'],
                           link1=recommend_job_1['link'],
                           desc2=recommend_job_2['summary'],
                           job2=recommend_job_2['title'],
                           link2=recommend_job_2['link'],
                           desc3=recommend_job_3['summary'],
                           job3=recommend_job_3['title'],
                           link3=recommend_job_3['link'],
                           desc4=recommend_job_4['summary'],
                           job4=recommend_job_4['title'],
                           link4=recommend_job_4['link'],
                           desc5=recommend_job_5['summary'],
                           job5=recommend_job_5['title'],
                           link5=recommend_job_5['link'])


@bp.route("/test", methods=["GET", "POST"])
def summary_test():

    return render_template("summary.html")


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

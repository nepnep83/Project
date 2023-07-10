from flask import render_template, request, redirect, url_for, session, flash, make_response
import json
from app.main import bp
from app.main.forms import CookiesForm, JobTitle, PrefJob, Postcode

from Backend import job_vacancies

NO_JOBS_FOUND_MESSAGE = "We could not find any recommended jobs for you at the moment, please try again later."

user_info = "user_info"
user_account = "user_account"


@bp.route("/", methods=["GET", "POST"])
def index():
    jobs = []
    form = JobTitle()
    if form.validate_on_submit():
        if form['radio'].data == 'yes':
            for i in range(1, 6):
                if form["job_title_" + str(i)].data:
                    jobs.append(form["job_title_" + str(i)].data)
            session["job_titles"] = jobs
        else:
            session['job_titles'] = []

        return redirect(url_for("main.preferred"))
    return render_template("index.html", form=form)


@bp.route("/preferred", methods=["GET", "POST"])
def preferred():
    form = PrefJob()
    if form.validate_on_submit():
        if form['radio'].data == 'yes':
            session['pref_job'] = form.pref_job.data
        else:
            session['pref_job'] = ''
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
    return render_template("summary.html", job_titles=session['job_titles'], pref_job=session['pref_job'],
                           postcode=session['postcode'])


@bp.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    jobs = session['job_titles']
    interest = session['pref_job']
    provided_postcode = session['postcode']
    message = ''
    pref_message = ''
    rows = []
    pref_rows = []
    if True:
        if len(jobs) > 0:
            recommend_job = job_vacancies.run(jobs, 10, provided_postcode, 5)

            recommend_job_1 = recommend_job[0]
            recommend_job_2 = recommend_job[1]
            recommend_job_3 = recommend_job[2]
            recommend_job_4 = recommend_job[3]
            recommend_job_5 = recommend_job[4]

            rows = [
                {'desc': recommend_job_1['summary'], 'job': recommend_job_1['title'], 'link': recommend_job_1['link']},
                {'desc': recommend_job_2['summary'], 'job': recommend_job_2['title'], 'link': recommend_job_2['link']},
                {'desc': recommend_job_3['summary'], 'job': recommend_job_3['title'], 'link': recommend_job_3['link']},
                {'desc': recommend_job_4['summary'], 'job': recommend_job_4['title'], 'link': recommend_job_4['link']},
                {'desc': recommend_job_5['summary'], 'job': recommend_job_5['title'], 'link': recommend_job_5['link']}]
        else:
            message = NO_JOBS_FOUND_MESSAGE

        if len(interest) > 0:
            preferred_job = job_vacancies.run(interest, 10, provided_postcode, 3)
            preferred_job_1 = preferred_job[0]
            preferred_job_2 = preferred_job[1]
            preferred_job_3 = preferred_job[2]

            pref_rows = [
                {'desc': preferred_job_1['summary'], 'job': preferred_job_1['title'],
                 'link': preferred_job_1['link']},
                {'desc': preferred_job_2['summary'], 'job': preferred_job_2['title'],
                 'link': preferred_job_2['link']},
                {'desc': preferred_job_3['summary'], 'job': preferred_job_3['title'],
                 'link': preferred_job_3['link']}]
        else:
            pref_message = NO_JOBS_FOUND_MESSAGE

    return render_template("recommendation.html", rows=rows, pref_rows=pref_rows, message=message,
                           pref_message=pref_message)


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

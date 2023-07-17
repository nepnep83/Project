from flask import render_template, request, redirect, url_for, session, flash, make_response
import json
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from Backend.job_vacancies import find_vacancies
from Backend.recommend_jobs import get_recommended_jobs
from app.main import bp
from app.main.forms import CookiesForm, JobTitle, PrefJob, Postcode

from Backend import job_vacancies, recommend_jobs

NO_JOBS_FOUND_MESSAGE = "We could not find any recommended jobs for you at the moment, please try again later."

user_info = "user_info"
user_account = "user_account"


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("main.html",)


@bp.route("/postcode", methods=["GET", "POST"])
def postcode():
    form = Postcode()
    if form.validate_on_submit():
        session['postcode'] = form.postcode.data
        return redirect(url_for("main.work_history"))
    return render_template("postcode.html", form=form)


@bp.route("/work_history", methods=["GET", "POST"])
def work_history():
    jobs = []
    form = JobTitle()
    session['message'] = ''
    session['rows'] = ''
    if form.validate_on_submit():
        if form['radio'].data == 'yes':
            for i in range(1, 6):
                if form["job_title_" + str(i)].data:
                    jobs.append(form["job_title_" + str(i)].data)
            session["job_titles"] = jobs
        else:
            session['job_titles'] = []

        if len(jobs) > 0:
            recommended_soc_codes = recommend_jobs.run(jobs)
            recommend_job = find_vacancies(10, session['postcode'], recommended_soc_codes, 5)
            session['titles'] = [get_recommended_jobs([recommended_soc_codes[i]], 1)[0] for i in range(5)]

            recommend_job_1 = recommend_job[0]
            recommend_job_2 = recommend_job[1]
            recommend_job_3 = recommend_job[2]
            recommend_job_4 = recommend_job[3]
            recommend_job_5 = recommend_job[4]

            session['rows'] = [
                {'desc': recommend_job_1['summary'], 'job': recommend_job_1['title'], 'link': recommend_job_1['link']},
                {'desc': recommend_job_2['summary'], 'job': recommend_job_2['title'], 'link': recommend_job_2['link']},
                {'desc': recommend_job_3['summary'], 'job': recommend_job_3['title'], 'link': recommend_job_3['link']},
                {'desc': recommend_job_4['summary'], 'job': recommend_job_4['title'], 'link': recommend_job_4['link']},
                {'desc': recommend_job_5['summary'], 'job': recommend_job_5['title'], 'link': recommend_job_5['link']}]
        else:
            session['message'] = NO_JOBS_FOUND_MESSAGE

        return redirect(url_for("main.preferred"))
    return render_template("work_history.html", form=form)


@bp.route("/preferred", methods=["GET", "POST"])
def preferred():
    form = PrefJob()
    session['pref_message'] = ''
    session['pref_rows'] = ''
    if form.validate_on_submit():
        if form['radio'].data == 'yes':
            session['pref_job'] = form.pref_job.data
            print(session['pref_job'])
        else:
            session['pref_job'] = ''

        if len(session['pref_job']) > 0:
            preferred_job = job_vacancies.run(session['pref_job'], 10, session['postcode'], 3)
            preferred_job_1 = preferred_job[0]
            preferred_job_2 = preferred_job[1]
            preferred_job_3 = preferred_job[2]

            session['pref_rows'] = [
                {'desc': preferred_job_1['summary'], 'job': preferred_job_1['title'],
                 'link': preferred_job_1['link']},
                {'desc': preferred_job_2['summary'], 'job': preferred_job_2['title'],
                 'link': preferred_job_2['link']},
                {'desc': preferred_job_3['summary'], 'job': preferred_job_3['title'],
                 'link': preferred_job_3['link']}]
        else:
            session['pref_message'] = NO_JOBS_FOUND_MESSAGE
        print(session)
        return redirect(url_for("main.summary"))
    return render_template("preferred.html", form=form)


@bp.route("/summary", methods=["GET", "POST"])
def summary():
    return render_template("summary.html", job_titles=session['job_titles'], pref_job=session['pref_job'],
                           postcode=session['postcode'])


@bp.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    return render_template("recommendation.html", titles=session['titles'], rows=session['rows'],
                           pref_rows=session['pref_rows'], message=session['message'],
                           pref_message=session['pref_message'])


@bp.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("accessibility.html")


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


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    return render_template(f"{error.code}.html"), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)

import threading

from flask import render_template, request, redirect, url_for, session, flash, make_response
import json
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from Backend.job_vacancies import get_vacancies_from_soc_codes, get_vacancies_from_titles
from app.main import bp
from app.main.forms import CookiesForm, JobTitle, PrefJob, Postcode

from Backend import recommend_jobs
from sql.vacancy_table import insert_history, delete_session_data, get_vacancy_rows

REFRESH_MESSAGE = "Vacancies are still being calculated. Please refresh."
ENTER_WORK_HISTORY = "Please enter work history to receive recommended job vacancies."
NOT_PROVIDED = "Not provided"
NO_JOBS_ENTERED = "Please provide {} in order to receive recommended job titles."

user_info = "user_info"
user_account = "user_account"


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("main.html", )


@bp.route("/postcode", methods=["GET", "POST"])
def postcode():
    form = Postcode()
    if form.validate_on_submit():
        session['postcode'] = form.postcode.data
        return redirect(url_for("main.work_history"))
    return render_template("postcode.html", form=form)


@bp.route("/work_history", methods=["GET", "POST"])
def work_history():
    form = JobTitle()
    delete_session_data(session['csrf_token'])
    if form.validate_on_submit():
        inputted_jobs = []

        session['message'] = ''
        session['rows'] = ''
        if form['radio'].data == 'yes':
            for i in range(1, 6):
                if form["job_title_" + str(i)].data:
                    inputted_jobs.append(form["job_title_" + str(i)].data)
            session["job_titles"] = inputted_jobs
        else:
            session["job_titles"] = []

        if len(inputted_jobs) > 0:
            recommended_soc_codes, recommended_titles = recommend_jobs.run(inputted_jobs)
            session['titles'] = recommended_titles
            thread = threading.Thread(target=task, args=(inputted_jobs, recommended_titles, recommended_soc_codes, session['postcode'], session['csrf_token']))
            thread.start()
        else:
            session['message'] = NO_JOBS_ENTERED.format("work history")
        return redirect(url_for("main.preferred"))
    return render_template("work_history.html", form=form)


@bp.route("/preferred", methods=["GET", "POST"])
def preferred():
    jobs = []
    form = PrefJob()
    session['pref_message'] = ''
    session['pref_rows'] = ''
    if form.validate_on_submit():
        if form['radio'].data == 'yes':
            for i in range(1, 6):
                if form["pref_job_" + str(i)].data:
                    jobs.append(form["pref_job_" + str(i)].data)
            session["pref_job_titles"] = jobs
        else:
            session["pref_job_titles"] = []

        if len(jobs) > 0:
            recommended_pref_soc_codes, recommended_pref_titles = recommend_jobs.run(jobs)
            session['pref_titles'] = recommended_pref_titles
        else:
            session['pref_message'] = NO_JOBS_ENTERED.format("preferred jobs")
        return redirect(url_for("main.summary"))
    return render_template("preferred.html", form=form)


@bp.route("/summary", methods=["GET", "POST"])
def summary():
    print(session)
    return render_template("summary.html",
                           job_titles=session['job_titles'] if session['job_titles'] != [] else [NOT_PROVIDED],
                           pref_job=session['pref_job_titles'] if session['pref_job_titles'] != [] else [NOT_PROVIDED],
                           postcode=session['postcode'])


@bp.route("/recommended_titles", methods=["GET", "POST"])
def recommended_titles():
    return render_template("recommended_titles.html",
                           titles=session['titles'],
                           pref_titles=session['pref_titles'] if 'pref_titles' in session.keys() else '',
                           message=session['message'],
                           pref_message=session['pref_message'])


@bp.route("/recommended_vacancies", methods=["GET", "POST"])
def recommended_vacancies():
    vacancy_rows = get_vacancy_rows(session['csrf_token'])
    error_message = ''
    if len(vacancy_rows) == 0:
        if session['message'] == '':
            error_message = REFRESH_MESSAGE
        else:
            error_message = ENTER_WORK_HISTORY

    return render_template("recommended_vacancies.html",
                           rows=vacancy_rows,
                           message=error_message)


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


def task(inputted_jobs, recommend_titles, recommended_soc_codes, current_postcode, session_id):
    recommended_jobs = []
    get_vacancies_from_titles(inputted_jobs, current_postcode, recommended_jobs)
    get_vacancies_from_titles(recommend_titles, current_postcode, recommended_jobs)
    get_vacancies_from_soc_codes(recommended_soc_codes, current_postcode, recommended_jobs)

    for recommend_job in recommended_jobs:
        insert_history(session_id, recommend_job['summary'], recommend_job['title'], recommend_job['link'])

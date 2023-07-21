from Backend import common
import time

from sql.soc_table import get_titles


def get_claimant_info():
    distance_inp = input('Input how far you are willing to travel for work in miles ')
    location_inp = input('Input the first half of your postcode (eg. SE1) ')

    return distance_inp, location_inp


def is_at_least_one_vacancy_nationally(job):
    return call_vacancy_api(job) is not None


def call_vacancy_api(title, postcode=None, travel_distance=None):
    vacancies = "too many calls"
    while vacancies == "too many calls":
        vacancies = common.api_call(
            "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5"
            + ("&radius=" + str(travel_distance) if travel_distance is not None else "")
            + ("&location=" + postcode if postcode is not None else "")
            + ("&keywords=" + title)
        )
        if vacancies == "too many calls":
            time.sleep(15)
        else:
            time.sleep(1)
    return vacancies[0] if type(vacancies) is list and len(vacancies) > 0 else None


def get_vacancies_from_titles(titles, postcode, recommended_jobs):
    for title in titles:
        if len(recommended_jobs) < 5:
            recommended = call_vacancy_api(title, postcode, 10)
            if recommended and recommended['title'] not in [recommended_job['title'] for recommended_job in recommended_jobs]:
                recommended_jobs.append(recommended)


def get_vacancies_from_soc_codes(recommended_soc_codes, postcode, recommended_jobs):
    if len(recommended_jobs) < 5:
        for soc_code in recommended_soc_codes:
            job_titles = get_titles(soc_code)
            current_title_counter = 0
            vacancies = None
            while (vacancies is None or vacancies == "not found") and current_title_counter < len(job_titles):
                vacancies = call_vacancy_api(job_titles[current_title_counter], postcode, 10)

                if vacancies is not None and type(vacancies) is list and vacancies[0]['title'] not in [recommended_job['title'] for recommended_job in recommended_jobs]:
                    recommended_jobs.append(vacancies[0])
                    if len(recommended_jobs) >= 5:
                        return
                else:
                    current_title_counter += 1

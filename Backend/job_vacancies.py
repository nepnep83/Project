from Backend import common
from Backend import recommend_jobs
import time

from sql.soc_table import get_titles

_range = 10
interests_range = 5
job_range = 5


def get_claimant_info():
    distance_inp = input('Input how far you are willing to travel for work in miles ')
    location_inp = input('Input the first half of your postcode (eg. SE1) ')

    return distance_inp, location_inp


def is_at_least_one_vacancy_nationally(job):
    try:
        vacancies = "error"
        while vacancies == "error":
            vacancies = common.api_call(
                "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=1&keywords=" + job)
            time.sleep(2)
        if len(vacancies) > 0:
            return True
        else:
            print("No job found")
    except Exception as e:
        print(e)

    return False


def call_vacancy_api(travel_distance, postcode, title):
    vacancies = "too many calls"
    while vacancies == "too many calls":
        vacancies = common.api_call(
            "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + str(
                travel_distance) + "&location=" + postcode + "&keywords=" + title)
        time.sleep(1)
    return vacancies[0] if len(vacancies) > 0 else None


def get_vacancies_from_titles(titles, postcode, recommended_jobs):
    for title in titles:
        if len(recommended_jobs) < 5:
            recommended = call_vacancy_api(10, postcode, title)
            if recommended and recommended['title'] not in [recommended_job['title'] for recommended_job in recommended_jobs]:
                recommended_jobs.append(recommended)


def get_vacancies_from_soc_codes(recommended_soc_codes, postcode, recommended_jobs):
    if len(recommended_jobs) < 5:
        for soc_code in recommended_soc_codes:
            job_titles = get_titles(soc_code)
            current_title_counter = 0
            try:
                vacancies = "too many calls"
                while vacancies == "too many calls" or vacancies == "not found" or len(vacancies) == 0:
                    vacancies = common.api_call(
                        "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=10&location=" + postcode
                        + "&keywords=" + job_titles[current_title_counter])
                    time.sleep(1)
                    if vacancies == "not found" or len(vacancies) == 0:
                        current_title_counter += 1
                    elif vacancies == "too many calls":
                        time.sleep(15)
                if vacancies[0]['title'] not in [recommended_job['title'] for recommended_job in recommended_jobs]:
                    recommended_jobs.append(vacancies[0])
                if len(recommended_jobs) >= 5:
                    return recommended_jobs
                else:
                    print("Not enough jobs have been found yet")
            except Exception as e:
                print(e)


def run(jobs, distance_to_job, location_of_claimant, _range):
    recommended_soc_codes = recommend_jobs.run(jobs)
    local_jobs_experience = get_vacancies_from_soc_codes(distance_to_job, location_of_claimant, recommended_soc_codes)

    return local_jobs_experience


if __name__ == "__main__":
    distance, location = get_claimant_info()
    place_holder_job = ['plumber']
    run(place_holder_job, distance, location, job_range)

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


def find_vacancies(travel_distance, postcode, recommended_soc_codes, job_num):
    found_vacancies = []
    for soc_code in recommended_soc_codes:
        job_titles = get_titles(soc_code)
        current_title_counter = 0
        try:
            vacancies = "too many calls"
            while vacancies == "too many calls" or vacancies == "not found" or len(vacancies) == 0:
                vacancies = common.api_call(
                    "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + str(
                        travel_distance) + "&location=" + postcode + "&keywords=" + job_titles[current_title_counter])
                time.sleep(1)
                if vacancies == "not found" or len(vacancies) == 0:
                    current_title_counter += 1
            found_vacancies.append(vacancies[0])
            if len(vacancies) > 1:
                found_vacancies.append(vacancies[1])
            if len(found_vacancies) >= job_num:
                return found_vacancies
            else:
                print("Not enough jobs have been found yet")
        except Exception as e:
            print(e)

    return found_vacancies


def run(jobs, distance_to_job, location_of_claimant, _range):
    recommended_soc_codes = recommend_jobs.run(jobs)
    local_jobs_experience = find_vacancies(distance_to_job, location_of_claimant, recommended_soc_codes, _range)

    print("local_jobs_experience ", local_jobs_experience)
    return local_jobs_experience


if __name__ == "__main__":
    distance, location = get_claimant_info()
    place_holder_job = ['plumber']
    run(place_holder_job, distance, location, job_range)

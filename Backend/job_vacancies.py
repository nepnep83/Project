from Backend import common
from Backend import recommend_jobs
import time

_range = 10
interests_range = 5
job_range = 5


def get_claimant_info():
    distance = input('Input how far you are willing to travel for work in miles ')
    location = input('Input the first half of your postcode (eg. SE1) ')

    return distance, location


def get_recommend_jobs(jobs, interest):
    job, interests = recommend_jobs.run(jobs, interest, _range, interests_range, job_range)
    return job, interests


def find_vacancies(travel_distance, postcode, jobs, job_num):
    _jobs = []
    for job in jobs:
        try:
            time.sleep(1)
            vacancies = common.api_call(
                "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + str(
                    travel_distance) + "&location=" + postcode + "&keywords=" + job)
            print(vacancies)
            _jobs.append(vacancies[0])
            print(_jobs)
            if len(_jobs) >= job_num:
                return _jobs
            else:
                print("No job found")
        except Exception as e:
            print(e)

    return _jobs


def run(jobs, interests, distance, location, _range):
    recommended_jobs_experience, recommended_jobs_preferred = get_recommend_jobs(jobs, interests)
    local_jobs_experience = find_vacancies(distance, location, recommended_jobs_experience, _range)
    local_jobs_preferred = find_vacancies(distance, location, recommended_jobs_preferred, _range)

    print(local_jobs_experience)
    return local_jobs_experience, local_jobs_preferred


if __name__ == "__main__":
    distance, location = get_claimant_info()
    place_holder_job = ['plumber']
    place_holder_interest = ['engineer']
    run(place_holder_job, place_holder_interest, distance, location, job_range)

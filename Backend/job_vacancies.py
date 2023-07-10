from Backend import common
from Backend import recommend_jobs
import time

_range = 10
interests_range = 5
job_range = 5


def get_claimant_info():
    distance_inp = input('Input how far you are willing to travel for work in miles ')
    location_inp = input('Input the first half of your postcode (eg. SE1) ')

    return distance_inp, location_inp


def get_recommend_jobs(jobs):
    job = recommend_jobs.run(jobs, _range, job_range)
    return job


def find_vacancies(travel_distance, postcode, jobs, job_num):
    _jobs = []
    for job in jobs:
        try:
            time.sleep(1)
            vacancies = common.api_call(
                "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + str(
                    travel_distance) + "&location=" + postcode + "&keywords=" + job)
            print("vacancies ", vacancies)
            _jobs.append(vacancies[0])
            print("_jobs ", _jobs)
            print("job length " + str(len(_jobs)))
            if len(_jobs) >= job_num:
                return _jobs
            else:
                print("No job found")
        except Exception as e:
            print(e)

    return _jobs


def run(jobs, distance_to_job, location_of_claimant, _range):
    recommended_jobs_experience = get_recommend_jobs(jobs)
    local_jobs_experience = find_vacancies(distance_to_job, location_of_claimant, recommended_jobs_experience, _range)

    print("local_jobs_experience ", local_jobs_experience)
    return local_jobs_experience


if __name__ == "__main__":
    distance, location = get_claimant_info()
    place_holder_job = ['plumber']
    run(place_holder_job, distance, location, job_range)

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
    jobs = recommend_jobs.run(jobs, interest, _range, interests_range, job_range)
    return jobs


def find_vacancies(travel_distance, postcode, jobs):
    _jobs = []
    for job in jobs:
        try:
            time.sleep(0.5)
            vacancies = common.api_call(
                "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + str(
                    travel_distance) + "&location=" + postcode + "&keywords=" + job)
            if Exception != 'There seems to be a issue getting your job recommendations back to you, please try again later':
                _jobs.append(vacancies[0])
                if len(_jobs) >= 5:
                    return _jobs
        except:
            print('')

    return _jobs


def run(jobs, interests, distance, location, _range):
    recommended_jobs_experience, recommended_jobs_preferred = recommend_jobs.run(jobs, interests, _range,
                                                                                 interests_range, job_range)
    local_jobs_experience = find_vacancies(distance, location, recommended_jobs_experience)
    local_jobs_preferred = find_vacancies(distance, location, recommended_jobs_preferred)
    # for jobs in local_jobs:
    #   job = local_jobs[jobs]
    # for i in range(_range):
    #     print(local_jobs_experience[i]['title'])
    #     print(local_jobs_experience[i]['company'])
    #     print(local_jobs_experience[i]['link'], '\n')
    print(local_jobs_experience)
    return local_jobs_experience, local_jobs_preferred


if __name__ == "__main__":
    distance, location = get_claimant_info()
    place_holder_job = ['plumber']
    place_holder_interest = ['engineer']
    run(place_holder_job, place_holder_interest, distance, location, job_range)

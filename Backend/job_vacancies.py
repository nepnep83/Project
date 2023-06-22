from Backend import common
from Backend import recommend_jobs

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


def find_vacancies(travel_distance, postcode, job):
    vacancies = common.api_call(
        "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + str(travel_distance) + "&location=" + postcode + "&keywords=" + job[0])
    return vacancies


def run(jobs, interests, distance, location, _range):
    #recommended_jobs = get_recommend_jobs(jobs, interests)
    local_jobs = find_vacancies(distance, location, jobs)
    # for jobs in local_jobs:
    #   job = local_jobs[jobs]
    for i in range(_range):
        print(local_jobs[i]['title'])
        print(local_jobs[i]['company'])
        print(local_jobs[i]['link'], '\n')
    return local_jobs


if __name__ == "__main__":
    distance, location = get_claimant_info()
    place_holder_job = 'plumber'
    place_holder_interest = 'engineer'
    run(place_holder_job, place_holder_interest, distance, location, job_range)

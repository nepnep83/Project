import common
import recommend_jobs

job_range = 5


def get_claimant_info():
    distance = input('Input how far you are willing to travel for work in miles ')
    location = input('Input the first half of your postcode (eg. SE1) ')

    return distance, location


def get_recommend_jobs():
    jobs = recommend_jobs.run()
    return jobs


def find_vacancies(travel_distance, postcode, job):
    vacancies = common.api_call(
        "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=" + travel_distance + "&location=" + postcode + "&keywords=" + job)
    return vacancies


def run():
    place_holder_job = 'plumber'
    distance, location = get_claimant_info()
    # recommended_jobs = get_recommend_jobs()
    local_jobs = find_vacancies(distance, location, place_holder_job)
    # for jobs in local_jobs:
    #   job = local_jobs[jobs]
    for i in range(job_range):
        print(local_jobs[i]['title'])
        print(local_jobs[i]['company'])
        print(local_jobs[i]['link'], '\n')


if __name__ == "__main__":
    run()

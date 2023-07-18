import requests

from Backend import common


def get_claimants_jobs():
    jobs = [input("Input your previous job\n")]
    while True:
        a = input('Have you had any other jobs?')
        if a == 'Yes' or a == 'yes':
            jobs.append(input("Input your other job\n"))
        elif a == 'No' or a == 'no':
            break
        else:
            print('Invalid input, Please enter "Yes" or "No')
    return jobs


def get_claimants_interests():
    return [input("which job would you be interested in applying for?")]


def get_soc_code(job):
    soc_response = common.api_call('https://api.lmiforall.org.uk/api/v1/soc/search?q=' + str(job))
    if len(soc_response) == 0:
        raise Exception(job + " is not a valid input")
    else:
        return soc_response[0]['soc']


def soc_to_onet(soc):
    onet_response = common.api_call('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/' + str(soc))
    return onet_response['onetCodes'][0]['code']


def get_skills_from_onet_code(onet):
    skills_response = requests.get('https://api.lmiforall.org.uk/api/v1/o-net/skills/' + str(onet), verify=False)
    skills = skills_response.json()['scales'][0]['skills']
    skills.sort(reverse=True, key=common.key)
    minimum_value = skills[0]['value'] - 1
    return [skill for skill in skills if minimum_value <= skill['value']]


def add_new_skills_and_sort(skills, new_skills):
    skills_id = get_skills_ids(skills)

    for new_skill in new_skills:
        if new_skill['id'] in ['2.A.1.a', '2.A.1.c', '2.A.1.e']:
            new_skill['value'] *= 0.5

        if skills_id.count(new_skill['id']) == 0:
            skills_id.append(new_skill['id'])
            skills.append(new_skill)
        else:
            for skill in skills:
                if skill['id'] == new_skill['id']:
                    skill['value'] += new_skill['value']

    skills.sort(reverse=True, key=common.key)


def get_skills_ids(skills):
    return [skill['id'] for skill in skills]


def get_recommended_soc_codes(skills):
    recommended_soc_codes = []
    job_titles = []
    rev_results = common.api_call(
        'https://api.lmiforall.org.uk/api/v1/o-net/reversematch?weights=100%2C100%2C100%2C100&skills=' + ",".join(skills)
    )['results']
    for result in rev_results:
        recommended_soc_codes.extend(result['likely_soc_codes'])
        job_titles.append(result['title'])

    seen = set()
    seen_add = seen.add
    return [x for x in recommended_soc_codes if not (x in seen or seen_add(x))], [x for x in job_titles if not (x in seen or seen_add(x))][:5]


def get_recommended_jobs(recommended_soc_codes, no_of_jobs):
    recommended_jobs = []
    for soc_code in recommended_soc_codes[:no_of_jobs]:
        job_response = common.api_call('https://api.lmiforall.org.uk/api/v1/soc/code/' + str(soc_code))
        if job_response == "not found":
            return job_response
        job_titles = job_response['add_titles']
        recommended_jobs.append(job_response['title'])
        for job in job_titles:
            recommended_jobs.append(job)

    return recommended_jobs


def run(jobs):
    skills = []

    try:
        for job in jobs:
            soc = get_soc_code(job)
            onet = soc_to_onet(soc)

            new_skills = get_skills_from_onet_code(onet)
            add_new_skills_and_sort(skills, new_skills)

    except Exception as e:
        print(e)

    if skills:
        minimum_value = skills[0]['value'] - len(jobs)
        top_skills_ids = [skill['id'] for skill in skills if minimum_value <= skill['value']]
        return get_recommended_soc_codes(top_skills_ids)


if __name__ == "__main__":
    job_num = 5

    run(['Plumber', 'engineer', 'lawyer'], job_num)

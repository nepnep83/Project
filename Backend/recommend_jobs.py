import requests

from Backend import common


def get_claimants_jobs():
    jobs = []
    jobs.append(input("Input your previous job\n"))
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
    interests = []
    interests.append(input("which job would you be interested in applying for?"))
    return interests


def get_soc_code(job):
    soc_response = common.api_call('https://api.lmiforall.org.uk/api/v1/soc/search?q=' + str(job))
    if len(soc_response) == 0:
        raise Exception(job + " is not a valid input")
    else:
        soc = soc_response[0]['soc']
    return soc


def soc_to_onet(soc):
    onet_response = common.api_call('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/' + str(soc))
    onet_data = onet_response['onetCodes']
    onet = onet_data[0]['code']
    return onet


def onet_skills(onet, skill_list, _range):
    skills = []
    skills_data_ = []
    skills_response = requests.get('https://api.lmiforall.org.uk/api/v1/o-net/skills/' + str(onet), verify=False)
    skills_data = skills_response.json()['scales']
    skills_data3 = skills_data[0]
    skills_data4 = skills_data3['skills']
    skills_data4.sort(reverse=True, key=common.key)
    for i in range(_range):
        skills_data5 = skills_data4[i]
        skills_data_.append(skills_data5)
        skills.append(skills_data5['id'])
    skill_list = skill_sort(skills_data_, skill_list)

    return skill_list


def onet_interests(onet, _range):
    interests_data_ = []
    interests_response = common.api_call('https://api.lmiforall.org.uk/api/v1/o-net/interests/' + onet)
    interests_data = interests_response['scales']
    interests_data2 = interests_data[1]
    interests_data3 = interests_data2['interests']
    interests_data3.sort(reverse=True, key=common.key)
    for i in range(_range):
        interests_data4 = interests_data3[i]
        interests_data_.append(interests_data4)

    return interests_data_


def skill_sort(skills, skill_list):
    skill_id = get_ids(skill_list)
    for skill in skills:
        if skill_id.count(skill['id']) == 0:
            skill_id.append(skill['id'])
            skill_list.append(skill)
        else:
            for skilll in skill_list:
                if skilll['id'] == skill['id']:
                    skilll['value'] += skill['value']
    skill_list.sort(reverse=True, key=common.key)

    return skill_list


def get_ids(skills):
    skill_id = []
    for skill in skills:
        skill_id.append(skill['id'])
    return skill_id


def reverse_search(skills, interests):
    rev = []
    rev_response = common.api_call(
        'https://api.lmiforall.org.uk/api/v1/o-net/reversematch?weights=100%2C100%2C100%2C100&interests=' + ",".join(
            interests) + '&skills=' + ",".join(skills))
    rev_data = rev_response['results']
    for i in range(len(rev_data)):
        rev_data2 = rev_data[i]
        rev.append(rev_data2['likely_soc_codes'][0])
    return rev


def find_job(rev, job_num):
    jobs = []
    for i in range(job_num):
        job_response = common.api_call('https://api.lmiforall.org.uk/api/v1/soc/code/' + str(rev[i]))
        job_titles = job_response['add_titles']
        for job in job_titles:
            if job.find(",") != -1:
                x = job.split(",")
                text = (",".join(x[1:]) + " " + x[0])[1:]
            else:
                text = job
            jobs.append(text)

    print("Your recommended jobs are ", jobs)
    return jobs


def run(jobs, interests, _range, interests_range, job_num):
    skill_list = []
    top_skills = []
    top_interests = []
    skills_for_interests = []

    try:
        for job in jobs:
            soc = get_soc_code(job)
            onet = soc_to_onet(soc)

            skills_onet = onet_skills(onet, skill_list.copy(), _range)
            skill_list.extend(skills_onet)
        for interest in interests:
            soc = get_soc_code(interest)
            onet = soc_to_onet(soc)
            skills_for_interests = onet_interests(onet, interests_range)

    except Exception as e:
        print(e)
    for i in range(_range):
        top_skills.append(skill_list[i]['id'])
    for i in range(interests_range):
        top_interests.append(skills_for_interests[i]['id'])
    rev_experience = reverse_search(top_skills, '')
    rev_interest = reverse_search('', top_interests)
    jobs1 = find_job(rev_experience, job_num)
    jobs2 = find_job(rev_interest, job_num)
    return jobs1, jobs2


if __name__ == "__main__":
    _range = 15
    interests_range = 5
    job_num = 5

    # jobs = get_claimants_jobs()
    # interests = get_claimants_interests()

    run(['Plumber'], ["Engineer"], _range, interests_range, job_num)

import json
import requests

skill_list = []
skill_id = []
_range = 15


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


def get_soc_code(job):
    soc_response = api_call('https://api.lmiforall.org.uk/api/v1/soc/search?q=', str(job))
    if len(soc_response) == 0:
        raise Exception(job + " is not a valid input")
    else:
        soc = soc_response[0]['soc']
    return soc



def soc_to_onet(soc):
    onet_response = api_call('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/', str(soc))
    onet_data = onet_response['onetCodes']
    onet = onet_data[0]['code']
    return onet


def key(e):
    return e['value']


def reverse_search(skills):
    rev = []
    rev_response = api_call(
        'https://api.lmiforall.org.uk/api/v1/o-net/reversematch?weights=100%2C100%2C100%2C100&skills=', ",".join(
            skills))
    rev_data = rev_response['results']
    for i in range(len(rev_data)):
        rev_data2 = rev_data[i]
        rev.append(rev_data2['likely_soc_codes'][0])
    print(rev)
    return rev


def onet_skills(onet, _range):
    skills = []
    skills_data_ = []
    skills_response = requests.get('https://api.lmiforall.org.uk/api/v1/o-net/skills/' + str(onet),
                                   verify=False)
    skills_data = skills_response.json()['scales']
    skills_data3 = skills_data[0]
    skills_data4 = skills_data3['skills']
    skills_data4.sort(reverse=True, key=key)
    for i in range(_range):
        skills_data5 = skills_data4[i]
        skills_data_.append(skills_data5)
        skills.append(skills_data5['id'])
    a = skill_sort(skills_data_)

    return a


def skill_sort(skills):
    for skill in skills:
        if skill_id.count(skill['id']) == 0:
            skill_id.append(skill['id'])
            skill_list.append(skill)
        else:
            for skilll in skill_list:
                if skilll['id'] == skill['id']:
                    skilll['value'] += skill['value']
    skill_list.sort(reverse=True, key=key)
    return skill_id


def find_job(rev):
    job = []
    for i in range(5):
        job_response = api_call('https://api.lmiforall.org.uk/api/v1/soc/code/', str(rev[i]))
        job.append(job_response['title'])
    print("Your recommended jobs are ", job)
    return job


def api_call(link, var):
    response = requests.get(link + var, verify=False)
    if response.status_code == 200:
        data = response.text
        parse_json = json.loads(data)
    else:
        raise Exception(
            'There seems to be a issue getting your job recommendations back to you, please try again later')
    return parse_json


if __name__ == "__main__":
    onet = []
    skills = []
    top_skills = []
    jobs = get_claimants_jobs()
    try:
        for job in jobs:
            soc = get_soc_code(job)
            onet = (soc_to_onet(soc))
            skills.append(onet_skills(onet, _range))
    except Exception as e:
        print(e)

    for i in range(_range):
        top_skills.append(skill_list[i]['id'])
    rev = reverse_search(top_skills)
    find_job(rev)

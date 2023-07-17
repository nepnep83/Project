from Backend.job_vacancies import is_at_least_one_vacancy_nationally
from Backend.recommend_jobs import get_recommended_jobs
from sql.soc_table import get_num_checked, upsert_title, get_titles, upsert_num_checked, get_current_soc


def find_job_titles(soc_code, list_of_job_titles):
    current_num_checked = get_num_checked(soc_code)
    for current_count in range(current_num_checked, len(list_of_job_titles)):
        job_title = list_of_job_titles[current_count]
        print("Trying title " + job_title)
        if is_at_least_one_vacancy_nationally(job_title):
            upsert_title(soc_code, job_title, current_count+1)
            print(get_titles(soc_code))
        else:
            upsert_num_checked(soc_code, current_count+1)


def validate_and_run_soc_code(soc_code):
    list_of_job_titles = get_recommended_jobs([soc_code], 1)
    if list_of_job_titles != "not found":
        find_job_titles(soc_code, list_of_job_titles)
    else:
        print("code " + str(soc_code) + " was not valid")


if __name__ == "__main__":
    for soc_code in range(get_current_soc(), 10000):
        validate_and_run_soc_code(soc_code)

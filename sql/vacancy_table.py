from sql.sql_utils import SqlUtils

soc_table = SqlUtils("recommended_job_vacancies")


def insert_history(session_id, description, job_title, link):
    soc_table.insert(creat_dictionary(session_id, description, job_title, link))


def get_vacancy_rows(session_id):
    rows = soc_table.get({"session_id": session_id}, ["description", "job_title", "link"])
    rows = [{'desc': row[0], 'job': row[1], 'link': row[1]}
            for row in rows]
    return rows


def delete_session_data(session_id):
    soc_table.delete({"session_id": session_id})


def creat_dictionary(session_id, description, job_title, link):
    return {"session_id": session_id, "description": description, "job_title": job_title, "link": link}

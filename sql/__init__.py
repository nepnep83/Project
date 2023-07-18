import os
from sqlite3 import dbapi2

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


class SocToTitle:
    def __init__(self, dbfile, query):
        self.dbfile = dbfile
        self.last_key = None

        with dbapi2.connect(dbfile) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()


def get_soc_to_title():
    DATABASE = os.path.join(PROJECT_ROOT, 'soc_code')
    query = "CREATE TABLE IF NOT EXISTS soc_to_title (soc_code INT NOT NULL PRIMARY KEY, job_titles TEXT, num_checked INT)"
    return SocToTitle(DATABASE, query)


def get_job_vacancies():
    DATABASE = os.path.join(PROJECT_ROOT, 'recommended_job_vacancies')
    query = "CREATE TABLE IF NOT EXISTS recommended_job_vacancies (ID INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, description TEXT, job_title TEXT, link TEXT)"
    return SocToTitle(DATABASE, query)


if __name__ == "__main__":
    dbname = get_soc_to_title()

import os
from sqlite3 import dbapi2


class SocToTitle:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.last_key = None

        with dbapi2.connect(dbfile) as connection:
            cursor = connection.cursor()
            query = "CREATE TABLE IF NOT EXISTS soc_to_title (soc_code INT NOT NULL PRIMARY KEY, job_titles TEXT, num_checked INT)"
            cursor.execute(query)
            connection.commit()


def get_soc_to_title():
    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
    DATABASE = os.path.join(PROJECT_ROOT, 'soc_code')
    return SocToTitle(DATABASE)


if __name__ == "__main__":
    dbname = get_soc_to_title()

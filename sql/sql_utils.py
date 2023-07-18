from sqlite3 import dbapi2

from sql import get_soc_to_title, get_job_vacancies


class SqlUtils:
    def __init__(self, table_title):
        if table_title == "soc_to_title":
            self.db = get_soc_to_title()
        elif table_title == "recommended_job_vacancies":
            self.db = get_job_vacancies()
        self.table_title = table_title

    def insert(self, dictionary_to_insert):
        with dbapi2.connect(self.db.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO {} ({}) VALUES ({})" \
                .format(self.table_title,
                        list_to_comma_string(list(dictionary_to_insert.keys())),
                        list_to_comma_string(["?"] * len(dictionary_to_insert)))
            cursor.execute(query, dic_values_to_tuple(dictionary_to_insert))
            connection.commit()
            self.db.last_key = cursor.lastrowid

    def update(self, dictionary_to_find, dictionary_to_update):
        dictionary_to_find = add_equals_to_dict_keys(dictionary_to_find)
        dictionary_to_update = add_equals_to_dict_keys(dictionary_to_update)

        with dbapi2.connect(self.db.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE {} SET {} WHERE {}" \
                .format(self.table_title,
                        list_to_comma_string(list(dictionary_to_update.keys())),
                        str(list(dictionary_to_find.keys())[0]))
            cursor.execute(query,
                           dic_values_to_tuple(dictionary_to_update) + dic_values_to_tuple(dictionary_to_find))
            connection.commit()

    def get(self, dictionary_to_find, list_to_get):
        dictionary_to_find = add_equals_to_dict_keys(dictionary_to_find)

        with dbapi2.connect(self.db.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT {} FROM {} WHERE {}" \
                .format(list_to_comma_string(list_to_get),
                        self.table_title,
                        str(list(dictionary_to_find.keys())[0]))
            cursor.execute(query, dic_values_to_tuple(dictionary_to_find))
            gotten = cursor.fetchall()
        return gotten

    def delete(self, dictionary_to_delete):
        dictionary_to_find = add_equals_to_dict_keys(dictionary_to_delete)

        with dbapi2.connect(self.db.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM {} WHERE {}" \
                .format(self.table_title,
                        str(list(dictionary_to_find.keys())[0]))
            cursor.execute(query, dic_values_to_tuple(dictionary_to_find))
            gotten = cursor.fetchone()
        return gotten

    def get_highest_row(self, orderColumn):
        with dbapi2.connect(self.db.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM soc_to_title ORDER BY {} DESC LIMIT 1" \
                .format(orderColumn)
            cursor.execute(query)
            last = cursor.fetchone()
        return last


def list_to_comma_string(list_values):
    return ', '.join(list(list_values))


def dic_values_to_tuple(dictionary):
    return tuple(dictionary.values(), )


def add_equals_to_dict_keys(dictionary):
    return dict((key + " = ?", value) for (key, value) in dictionary.items())

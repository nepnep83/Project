from sql.sql_utils import SqlUtils

soc_table = SqlUtils("soc_to_title")


def insert_title(soc_code, job_title, num_checked):
    soc_table.insert(creat_dictionary(soc_code, job_title, num_checked))


def insert_num_checked(soc_code, num_checked):
    soc_table.insert(creat_dictionary(soc_code, None, num_checked))


def update_title(soc_code, job_titles, num_checked):
    soc_table.update({"soc_code": soc_code}, {"job_titles": job_titles, "num_checked": num_checked})


def update_num_checked(soc_code, num_checked):
    soc_table.update({"soc_code": soc_code}, {"num_checked": num_checked})


def get_titles(soc_code):
    titles = soc_table.get({"soc_code": soc_code}, ["job_titles"])
    return titles[0][0].split(';') if (titles is not None and titles[0] is not None) else []


def get_num_checked(soc_code):
    num_checked = soc_table.get({"soc_code": soc_code}, ["num_checked"])
    return num_checked[0] if num_checked is not None else 0


def get_current_soc():
    current_soc = soc_table.get_highest_row("soc_code")
    return current_soc[0] if current_soc is not None else 0


def upsert_title(soc_code, found_job_title, num_checked):
    current_job_titles = get_titles(soc_code)
    if get_num_checked(soc_code) == 0:
        insert_title(soc_code, found_job_title, num_checked)
    else:
        current_job_titles.append(found_job_title)
        update_title(soc_code, ";".join(current_job_titles), num_checked)


def upsert_num_checked(soc_code, num_checked):
    current_num_checked = get_num_checked(soc_code)
    if current_num_checked == 0:
        insert_num_checked(soc_code, num_checked)
    else:
        update_num_checked(soc_code, num_checked)


def creat_dictionary(soc_code, job_title, num_checked):
    return {"soc_code": soc_code, "job_titles": job_title, "num_checked": num_checked}

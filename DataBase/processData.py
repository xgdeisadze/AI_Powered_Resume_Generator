import json
import sqlite3


def add_rapid_api_job_search2_to_db(file_name: str, cursor: sqlite3.Cursor):
    insert_statement = """INSERT OR IGNORE INTO jobs_listings
            (job_id, created_at, updated_at, job_title, job_description, seniority, full_time,
            location, company_name, salary, country, url, applicants_count)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    with open(file_name, "r") as data_file:
        all_lines = data_file.readlines()
        for line in all_lines:
            data = json.loads(line)
            for job in data:
                job_tuple = (
                    job.get("id"),
                    job.get("datePosted"),
                    job.get("datePosted"),
                    job.get("title"),
                    job.get("description"),
                    "NOT PROVIDED",
                    job.get("employmentType"),
                    job.get("location"),
                    job.get("company"),
                    job.get("salaryRange"),
                    "NOT PROVIDED",
                    job.get("jobProviders")[0]["url"],
                    "NOT AVAILABLE",
                )
                cursor.execute(insert_statement, job_tuple)


def add_rapid_results_to_db(file_name: str, cursor: sqlite3.Cursor):
    insert_statement = """INSERT OR IGNORE INTO jobs_listings
                (job_id, created_at, updated_at, job_title, job_description, seniority, full_time,
                location, company_name, salary, country, url, applicants_count)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    with open(file_name, "r") as data_file:
        all_lines = data_file.readlines()
        for job_line in all_lines:
            data = json.loads(job_line)
            job_tuple = (
                data.get("id"),
                data.get("datePosted"),
                data.get("datePosted"),
                data.get("title"),
                data.get("description"),
                data.get("job_level"),
                data.get("job_type"),
                data.get("location"),
                data.get("company"),
                f"{data.get('min_amount')} - {data.get('max_amount')}",
                "US",
                data.get("job_url_direct"),
                "NOT PROVIDED",
            )
            cursor.execute(insert_statement, job_tuple)


def get_jobs_from_db(cursor: sqlite3.Cursor) -> list[dict]:
    select_statement = """SELECT job_id, created_at, updated_at, job_title, job_description, seniority, full_time,
                location, company_name, salary, country, url, applicants_count FROM jobs_listings"""
    cursor.execute(select_statement)
    results = cursor.fetchall()
    jobs_listings = []
    for result in results:
        job_data = {}
        job_data["job_id"] = result[0]
        job_data["created_at"] = result[1]
        job_data["updated_at"] = result[2]
        job_data["job_title"] = result[3]
        job_data["job_description"] = result[4]
        job_data["seniority"] = result[5]
        job_data["full_time"] = result[6]
        job_data["location"] = result[7]
        job_data["company_name"] = result[8]
        job_data["salary"] = result[9]
        job_data["country"] = result[10]
        job_data["url"] = result[11]
        job_data["applicants_count"] = result[12]
        jobs_listings.append(job_data)
    return jobs_listings

def get_users_from_db(cursor: sqlite3.Cursor) -> list[dict]:
    select_statement = """SELECT userID, email, phone, name, github, other_link, projects, classes, other"""
    cursor.execute(select_statement)
    results = cursor.fetchall()
    user_profile = []
    for result in results:
        user_data = {}
        user_data["userID"] = result[0]
        user_data["email"] = result[0]
        user_data["phone"] = result[0]
        user_data["name"] = result[0]
        user_data["github"] = result[0]
        user_data["other_link"] = result[0]
        user_data["projects"] = result[0]
        user_data["classes"] = result[0]
        user_data["other"] = result[0]
    return user_profile
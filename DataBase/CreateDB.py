import sqlite3
import DataBase.DBUtils


def createDB(cursor: sqlite3.Cursor):

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS jobs_listings(
    job_id INT PRIMARY KEY,
    created_at TEXT,
    updated_at TEXT,
    job_title TEXT NOT NULL,
    job_description TEXT DEFAULT "",
    seniority TEXT,
    full_time TEXT,
    location TEXT NOT NULL,
    company_name TEXT NOT NULL,
    salary INT DEFAULT 0,
    country TEXT NOT NULL,
    url TEXT NOT NULL,
    applicants_count TEXT);"""
    )
    add_personal_info_Table(cursor)
    add_selected_user_Table(cursor)
    add_selected_job_Table(cursor)


def add_locations_Table(cursor: sqlite3.Cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS city_locations(
    city_name TEXT PRIMARY KEY,
    latitude REAL,
    longitude REAL);
    """
    )


def add_personal_info_Table(cursor: sqlite3.Cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS personal_info(
    userID TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    name TEXT NOT NULL,
    github TEXT,
    other_link TEXT,
    projects TEXT,
    classes TEXT,
    other TEXT
    );
    """
    )

def add_selected_user_Table(cursor: sqlite3.Cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS selected_user(
    userID TEXT PRIMARY KEY,
    email TEXT,
    phone TEXT,
    name TEXT,
    github TEXT,
    other_link TEXT,
    projects TEXT,
    classes TEXT,
    other TEXT);"""
    )

def add_selected_job_Table(cursor: sqlite3.Cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS selected_job(
    job_id INT PRIMARY KEY,
    created_at TEXT,
    updated_at TEXT,
    job_title TEXT,
    job_description TEXT DEFAULT "",
    seniority TEXT,
    full_time TEXT,
    location TEXT,
    company_name TEXT,
    salary INT DEFAULT 0,
    country TEXT,
    url TEXT,
    applicants_count TEXT);"""
    )


def main():
    conn, cursor = DataBase.DBUtils.open_db("Data/JobsAppDB.sqlite3")
    createDB(cursor)
    add_locations_Table(cursor)
    DataBase.DBUtils.close_db(conn)


if __name__ == "__main__":
    main()
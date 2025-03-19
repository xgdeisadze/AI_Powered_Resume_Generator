import json
import os
import DataBase.CreateDB
import GUI.EnterPersonalDataWindow
from DataBase import processData
from GUI.JobsWindow import get_complete_job_data
from PySide6.QtWidgets import QApplication
import API_Secrets
from google import genai
from os import path
from DataBase.DBUtils import open_db


DB_FILE = "Test.db"
JSON_FILE = "Test.json"
test_data = [  # again if we had discussed fixtures, I would do this in a cleaner manner
    {
        "id": "137d56fc45579232",
        "site": "indeed",
        "job_url_direct": "https://www.indeed.com/viewjob?jk=137d56fc45579232",
        "title": "Workday Finance Integrations Analyst",
        "company": "CommuniCare Health Services",
        "location": "Lewis Center, OH, US",
        "job_type": "fulltime",
        "date_posted": "2024-09-04",
        "salary_source": "direct_data",
        "interval": "yearly",
        "min_amount": "73499.0",
        "max_amount": "93066.0",
        "currency": "USD",
        "is_remote": "True",
        "job_level": "",
        "job_function": "",
        "company_industry": "",
        "listing_type": "",
        "emails": "",
        "description": "Big Long Description",
        "ceo_name": "Stephen L. Rosedale",
    },
    {
        "id": "34fvsdfy6df5676546",
        "site": "inword",
        "job_url_direct": "https://www.sillyurl.com/3456tsgert",
        "title": "Super Duper Dev",
        "company": "Big Tech Inc",
        "location": "Bridgewater MA",
        "job_type": "fulltime",
        "date_posted": "2024-09-04",
        "salary_source": "direct_data",
        "interval": "yearly",
        "min_amount": "70000.0",
        "max_amount": "80000.0",
        "currency": "USD",
        "is_remote": "True",
        "job_level": "",
        "job_function": "",
        "company_industry": "",
        "listing_type": "",
        "emails": "",
        "description": "Looking for new grad who wants to learn on the job and do lots of stuff",
        "ceo_name": "Big Wig BSU Grad",
    },
]


def test_create_DB():
    # first make sure that any previous database files are gone so that we are sure the current test is on a new db
    #   if os.path.exists(DB_FILE):
    #       os.remove(DB_FILE)
    # call the 'function under test'
    conn, cursor = DataBase.DBUtils.open_db(DB_FILE)
    DataBase.CreateDB.createDB(cursor)
    DataBase.DBUtils.close_db(conn)
    # now we are sure whatever is in the DB is brand new so if the right table is in the DB, it is because we put it there
    conn, cursor = DataBase.DBUtils.open_db(DB_FILE)
    result_set = cursor.execute(
        "Select * from sqlite_master where name='jobs_listings';"
    )
    assert len(result_set.fetchall()) == 1


def test_load_job_data():
    # I am relying on the fact that tests are run in order by pytest unless you tell it to try to parallelize
    # so the test above will have run and provide us with a brand new empty database with one table
    make_test_json_file()
    conn, cursor = DataBase.DBUtils.open_db(DB_FILE)
    processData.add_rapid_results_to_db(JSON_FILE, cursor)
    conn.commit()
    # DataBase.DBUtils.close_db(conn)  # we need to force a commit
    # conn, cursor = DataBase.DBUtils.open_db(DB_FILE) # now we can test
    cursor.execute("select count(*) from jobs_listings")
    result = cursor.fetchone()
    assert result[0] == len(
        test_data
    )  # fetch one will return a tuple - the count result tuple has only one item
    cursor.execute("select * from jobs_listings")
    result = cursor.fetchall()
    assert (
        result[-1][3] == test_data[-1]["title"]
    )  # I picked the title as the data item I am assuring is correct
    DataBase.DBUtils.close_db(conn)


def make_test_json_file():
    # if this were a real production solution I would use pytest fixtures, but since we haven't talked about them in
    # the course, I'll do this cheap way instead
    # as before - make sure we begin the test suite clean each time.
    if os.path.exists(JSON_FILE):
        os.remove(JSON_FILE)

    with open(JSON_FILE, "w") as out_file:
        for data in test_data:
            json.dump(data, out_file)
            out_file.write("\n")


def test_get_full_data():
    conn, cursor = DataBase.DBUtils.open_db(DB_FILE)
    jobs_data = processData.get_jobs_from_db(cursor)
    DataBase.DBUtils.close_db(conn)
    result = get_complete_job_data(jobs_data, "34fvsdfy6df5676546")
    assert result["full_time"] == "fulltime"
    assert result["job_title"] == "Super Duper Dev"
    assert (
        result["salary"]
        == f"{test_data[1].get('min_amount')} - {test_data[1].get('max_amount')}"
    )


def test_save_personal_data():
    conn, cursor = DataBase.DBUtils.open_db(DB_FILE)
    app = QApplication([])
    app.setApplicationName("test")
    mock_window = GUI.EnterPersonalDataWindow.PersonalDataWindow(cursor)
    mock_window.user_name.setText("Professor_Test")
    mock_window.user_email.setText("ptest@bridgew.edu")
    mock_window.phone.setText("508-531-2226")
    mock_window.name.setText("Professor Test T. Fellow")
    mock_window.github.setText("https://github.com/Professor_Test")
    mock_window.other_link.setText("https://www.linkedin.com/in/professor-test")
    mock_window.projects.setText(
        """
    DownEast Technology (3 years)
    team delivered an app for sales people to enter, track and synch full spectrum sales data, saving it both locally
    in the sales persons device and synching it to the company so that nothing is lost and multiple sales people working
    the same lead don't waste time covering the same ground. App built in C++ with significant SQL component

    Weston Books (2 years)
    Built an inventory management and cash register program for a bookstore in golang. Program used a bar code reader
    to read ISBN numbers from the bar codes and queried book API to auto fill most field when stocking books. Data stored
    in SQL database. Application produced PDF reports for inventory, sales and more.

    WheresMyJob.com (3 years)
    Delivered an application that pulled data from jobs APIs and displayed them on a map, displaying full data when
    a job was selected by the user. Users filter jobs to not be overwhelmed. App written using python, pandas, plotly, dash,
    geopy, requests and postgresql database. AI integration helps users auto generate resumes from a set of skills and a
    selected job.

    """
    )
    mock_window.classes.setText(
        """
        AI
        Theory of Computation
        Cognitive Science
        Algorithms
        Software Engineering
        Comparative Programming Languages
        Operating Systems
        Robotics
        Natural Language Processing
        Linguistics
        Compilers
        """
    )
    mock_window.other_info.setText("")
    # calling function under test!!
    GUI.EnterPersonalDataWindow.save(mock_window, cursor)
    cursor.execute(
        """select github, projects, classes, name from personal_info
    WHERE userID == ?""",
        (mock_window.user_name.text(),),
    )
    result = cursor.fetchone()
    assert result[0] == mock_window.github.text()
    assert result[1] == mock_window.projects.toPlainText()
    assert result[2] == mock_window.classes.toPlainText()
    assert result[3] == mock_window.name.text()
    DataBase.DBUtils.close_db(conn)

def test_llm_query():
    client = genai.Client(api_key=API_Secrets.gemini_api_key)

    prompt = """Send a Hello."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    assert response is not None, "Response is None"

def test_prompt_contains_info():
    conn, cursor = open_db(path.join("../Data", "JobsAppDB.sqlite3"))
    cursor.execute("SELECT job_description FROM selected_job")
    selected_job = cursor.fetchone()
    selected_job_string = selected_job[0]

    cursor.execute("SELECT * FROM selected_user")
    selected_user = cursor.fetchone()
    selected_user_dict = {
        "User_ID": selected_user[0],
        "E-Mail": selected_user[1],
        "Phone": selected_user[2],
        "Name": selected_user[3],
        "Github": selected_user[4],
        "Other_Links": selected_user[5],
        "Projects": selected_user[6],
        "Classes": selected_user[7],
        "Other": selected_user[8]
    }

    prompt = f"""Build a markdown resume for a job with the following job description: {selected_job_string}
    For an applicant with the following information: {selected_user_dict}
    Do not add random, unknown information. Create the resume solely on what information is given."""

    assert selected_job_string in prompt
    assert str(selected_user_dict) in prompt

def test_pdf_generated():
    # Change the working directory to the project root (one level up from 'tests')
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    resume_pdf_path = "ResumeGeneration/resume.pdf"
    cover_letter_pdf_path = "ResumeGeneration/cover_letter.pdf"

    # Ensure PDF files exist
    assert os.path.isfile(resume_pdf_path)
    assert os.path.isfile(cover_letter_pdf_path)


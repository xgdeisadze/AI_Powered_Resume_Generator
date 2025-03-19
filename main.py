from DataBase.CreateDB import createDB, add_personal_info_Table
from DataBase.DBUtils import open_db
from DataBase import processData
from os import path
import PySide6
import sys
from GUI import JobsWindow


def main():
    conn, cursor = open_db(path.join("Data", "JobsAppDB.sqlite3"))
    # Clear the selected user and selected job tables
    cursor.execute("DELETE FROM selected_user;")
    cursor.execute("DELETE FROM selected_job;")
    conn.commit()
    createDB(cursor)
    add_personal_info_Table(cursor)
    processData.add_rapid_results_to_db("rapidResults.json", cursor)
    processData.add_rapid_api_job_search2_to_db("rapid_jobs2.json", cursor)
    # end consider removing.
    jobs_data = processData.get_jobs_from_db(cursor)
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)
    jobs_window = JobsWindow.JobsWindow(jobs_data, conn, cursor)
    jobs_window.show()
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()

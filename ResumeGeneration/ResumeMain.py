from google import genai
import API_Secrets
from DataBase.DBUtils import open_db
from os import path
from md2pdf.core import md2pdf

conn, cursor = open_db(path.join("../Data", "JobsAppDB.sqlite3"))

def get_user_information():
    cursor.execute("SELECT * FROM selected_user")
    selected_user = cursor.fetchone()
    selected_user_dict = {
        "User_ID" : selected_user[0],
        "E-Mail" : selected_user[1],
        "Phone" : selected_user[2],
        "Name" : selected_user[3],
        "Github" : selected_user[4],
        "Other_Links" : selected_user[5],
        "Projects": selected_user[6],
        "Classes": selected_user[7],
        "Other": selected_user[8]
    }
    return selected_user_dict

def get_job_information():
    cursor.execute("SELECT * FROM selected_job")
    selected_job = cursor.fetchone()
    selected_job_dict = {
        "Job_ID": selected_job[0],
        "Created_At": selected_job[1],
        "Updated_At": selected_job[2],
        "Job_Title": selected_job[3],
        "Job_Description": selected_job[4],
        "Seniority": selected_job[5],
        "Full_Time": selected_job[6],
        "Location": selected_job[7],
        "Company_Name": selected_job[8],
        "Salary": selected_job[9],
        "Country": selected_job[10],
        "URL": selected_job[11],
        "Applicants_Count": selected_job[12]
    }
    return selected_job_dict

def google_generate_resume():
    user_info = get_user_information()
    job_info = get_job_information()

    client = genai.Client(api_key=API_Secrets.gemini_api_key)
    prompt = f"""Build a markdown resume for a job with the following information: {job_info}
    For an applicant with the following information: {user_info}
    Do not add random, unknown information. Create the resume solely on what information is given."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    if response.text:
        with open("resume.md", "w") as file:
            file.write(response.text[9:-3])  # Trim unnecessary metadata
    else:
        print("AI response was empty. Resume not generated.")

def google_generate_cover_letter():
    user_info = get_user_information()
    job_info = get_job_information()

    client = genai.Client(api_key=API_Secrets.gemini_api_key)
    prompt = f"""Build a markdown cover letter for a job with the following information: {job_info}
        For an applicant with the following information: {user_info}. 
        DO NOT add/create random qualifications/skills. Create the cover letter solely on what information is given
        to you about the user and the job"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    if response.text:
        with open("cover_letter.md", "w") as file:
            file.write(response.text[9:-3])  # Trim unnecessary metadata
    else:
        print("AI response was empty. Resume not generated.")


def main():
    google_generate_resume()
    google_generate_cover_letter()
    md2pdf("resume.pdf", md_file_path="resume.md")
    md2pdf("cover_letter.pdf", md_file_path="cover_letter.md")


if __name__ == "__main__":
    main()

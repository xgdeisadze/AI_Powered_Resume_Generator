import json
import requests
import random
from google import genai
from API_Secrets import API_KEY

client = genai.Client(api_key=API_KEY)

def generate_resume(job_description, personal_description):
    response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = f"""
    Job Description: {job_description}
    Personal Description: {personal_description}
    Please generate a resume in markdown format that fits this job description based on the personal description provided.
    """)
    return response.text

def fetch_job_data():
    response = requests.get('https://webhost.bridgew.edu/jsantore/Spring2025/Capstone/rapid_jobs2.json')

    if response.status_code == 200:
        try:
            raw_response = response.text

            # Create JSONDecoder instance to decode the response
            decoder = json.JSONDecoder(strict=False)

            # Initialize an empty list to store valid JSON objects and Keep Track of Index
            valid_json_data = []
            index = 0

            # Loop through raw response to extract multiple JSON objects if they exist
            while index < len(raw_response):
                try:
                    obj, index = decoder.raw_decode(raw_response, index)
                    valid_json_data.append(obj)
                except json.JSONDecodeError:
                    index += 1

            if valid_json_data and isinstance(valid_json_data[0], list):
                job_data = valid_json_data[0]
                random_job = random.choice(job_data)

                job_title = random_job.get('title', 'N/A')
                job_description = random_job.get('description', 'N/A')

                print("Job Title:", random_job.get('title', 'N/A'))
                print("Company:", random_job.get('company', 'N/A'))
                print("Location:", random_job.get('location', 'N/A'))
                print("Job Description:", random_job.get('description', 'N/A'))

                return job_title, job_description

            else:
                print("Error: Valid job data not found.")

        except Exception as e:
            print(f"Unexpected error occurred: {e}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

def main():
    # Get a random job's title and description
    job_title, job_description = fetch_job_data()

    if job_title and job_description:
        personal_description = """
        A highly motivated Computer Science student with a strong foundation in software engineering, algorithms, 
        machine learning, operating systems, and 2D game design. Proficient in Python and Java, with some 
        experience in C++ and Go. Currently working as a Software Automation Technician at Stryker, leveraging Squish
        and Python to develop automated tests, with nearly one year of industry experience. Strong problem-solving 
        skills and a passion for both technology and music, with expertise in multiple instruments and music production.
        """

        # Generate the resume
        resume = generate_resume(job_description, personal_description)
        print("\n")
        print("-" * 250)
        print("\n\nGenerated Resume in Markdown Format:")
        print(resume)

        # Save resume to a text file
        with open("generated_resume.txt", "w", encoding="utf-8") as file:
            file.write(resume)

    else:
        print("No job data available. Could not generate a resume.")


if __name__ == "__main__":
    main()

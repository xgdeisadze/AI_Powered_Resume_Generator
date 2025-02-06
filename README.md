# Xenia Deisadze - Project 1 Sprint 1

* **How to Run the Program:**
Running the program is fairly simple. Make sure to have the json, requests, random, and genai (_from google import genai_)
packages installed. I created a file, "API_Secrets", to store my API key. But, I included the file in git.ignore.
I'll have sent the API key to you privately. Just make sure to add the "API_Secrets" file and the "API_KEY" variable.
Other than that, just hit run and the program will randomly select a job, print out it's title, description, company,
and location. Then (after a few seconds), the AI will generate a resume. I separated the printed job information 
and the generated resume with a dashed line. Also, a generate_resume.txt file will be created.
Side Note: I had to include the certificates for the JSON Url in my certifi file.


* **Why I Chose Google Gemini/AI Studio:**
Honestly, it was free, easy to use, and the first option in the list of LLM's/AI's you provided.


* **Explains The AI Prompt that you Chose:**
I used "client.models.generate_content". I chose this after looking through the Gemini docs. Specifically, from this 
page: https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-generate-from-text-input#generativeaionvertexai_gemini_generate_from_text_input-python
.Then, within the response variable, I satisfied the "model" and "content" parameters by inputting the job_description, 
my personal description, and instructions for the AI. I used an f-string for this.
I tried a couple of different methods to start the API and get the response, but they didn't work out. For example, 
_"model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")"_ didn't work out.

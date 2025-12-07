# CSE476
Final Project for CSE 476


This project implements a basic agent that reads a list of questions from the file cse_476_final_project_test_data.json, sends each question to the API model, and saves the model’s answers in cse_476_final_project_answers.json.
The main script for the project is generate_answer_template.py.

# How the Agent Works
The script loads all questions from the test data file.
For each question, it calls the model using a simple function (model_call).
The model returns a short answer string.
The answer is added to a list and written to the output JSON file.
After all questions are answered, the script checks whether the output format is valid or not.

# Running the script

Download and connect to the ASU VPN or use ASU's wifi on campus, 
Download the required packages, run the following command :
pip install requests

Once that is done, run :
python generate_answer_template.py

When it finishes, it will create:
cse_476_final_project_answers.json

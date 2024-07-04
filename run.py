from flask import Flask, render_template, url_for, redirect, request
from main import *
import pandas as pd

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/job_list", methods=['GET', 'POST'])
def job_list():
    if request.method == 'POST':
        # Get data from the first form
        job = str(request.form['job'])
        experience = str(request.form['experience'])
        location = str(request.form['location'])
        skillsInput = str(request.form['skillsInput'])
        salaryInput = str(request.form['salaryInput'])

        # Process the form data (e.g., store it in a database, send an email)
        print(f"{job}, {experience}, location: {location}")
        print(f" skillsInput: {skillsInput}, salaryInput: {salaryInput}")

        # Optionally return a success message or redirect to another page
        return "Form submitted successfully!"

    file_path = r"job.csv"
    df = pd.read_csv(file_path)
    num_jobs = len(df)
    jobs = df.to_dict()
    jobs_per_page = 20
    page = request.args.get('page', 1, type=int)
    total_jobs = len(jobs['title'])
    total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

    start = (page - 1) * jobs_per_page
    end = start + jobs_per_page
    paginated_jobs = {key: {k: v for k, v in value.items() if start <= k < end} for key, value in jobs.items()}

    return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages, total_jobs=total_jobs)

if __name__ == "__main__":
    app.run(debug=True)
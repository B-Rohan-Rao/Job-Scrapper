from flask import Flask, render_template, url_for, redirect, request , session, make_response, flash
from main import *
import pandas as pd
import os
import numpy as np
from model import *


secretkey = os.urandom(24)

app = Flask(__name__, static_url_path='/static')
app.secret_key = secretkey


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/aisubmit',methods=['GET','POST'])
def aisubmit():
    if request.method == 'POST':
        no_of_jobs = request.form['no_jobs']
        return no_of_jobs


@app.route('/portal',methods=['GET','POST'])
def portal():
    if request.method == 'POST':
        portl = request.form['jobportal']
        session['jobportal'] = portl
        return portl
        

@app.route("/job_list", methods=['GET', 'POST'])
def job_list():
    data_fetched = True
    if request.method == 'POST':
        data_fetched = False
        # Get data from the first form
        job = (str(request.form['job']))
        experience = str(request.form['experience'])
        location = (str(request.form['location']))
        skillsInput = str(request.form['skillsInput'])
        salaryInput = str(request.form['salaryInput'])

        session['job'] = job
        session['experience'] = experience
        session['location'] = location
        session['skillsInput'] = skillsInput
        session['salaryInput'] = salaryInput
        print("Looking for {job}jobs at {location} for person with experience {experience}")

        jobs = search([job], [location], experience)
        data_fetched = True
        df = pd.DataFrame(jobs)
        df = df.sample(frac=1).reset_index(drop=True)
        jobs = {col: df[col].to_dict() for col in df.columns}

        jobs_per_page = 20
        page = request.args.get('page', 1, type=int)
        total_jobs = len(jobs['title'])
        total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

        start = (page - 1) * jobs_per_page
        end = start + jobs_per_page
        paginated_jobs = {key: {k: v for k, v in value.items() if start <= k < end} for key, value in jobs.items()}

        # Optionally return a success message or redirect to another page
        return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages, total_jobs=total_jobs, data_fetched = data_fetched)
    # return render_template('job_list.html')
    prtl = session.get('jobportal')
    print(prtl)

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

    return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages, total_jobs=total_jobs, data_fetched = data_fetched)

@app.route("/rec", methods = ["POST", "GET"])
def rec():
    try:
        title = session.get('job')
        skills = session.get('skillsInput')
        salary = session.get('salaryInput')

        df =  pd.read_csv('job.csv')
        dt = df.to_dict(orient='list')

        order = similar(dt, title, skills, salary)
        df = df.loc[df['index'].isin(order)].set_index('index').loc[order].reset_index()
        jobs = df.to_dict()

        jobs_per_page = 20
        page = request.args.get('page', 1, type=int)
        total_jobs = len(jobs['title'])
        total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

        start = (page - 1) * jobs_per_page
        end = start + jobs_per_page
        paginated_jobs = {key: {k: v for k, v in value.items() if start <= k < end} for key, value in jobs.items()}

        return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages,data_fetched = True)
    except:
        flash("Error: Unable to perform this operation. Please try again later.")
        return redirect(url_for('rec'))

if __name__ == "__main__":
    app.run(debug=True)
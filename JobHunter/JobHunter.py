# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# Brandon Bennett, babennett@student.rtc.edu (I NEVER CHECK THIS THING)(SLACK PLZ)(or message at 440-242-7914)
# CCNA337, Fall 2019

#Colaborated with Sam, Emily, Simeon, and Robin(who collaborated with others from his work)

#import....

import mysql.connector
#import sys
import json
import urllib.request
#import os
import time
from datetime import datetime


# Connect to database
# You may need to edit the connect function based on your local settings.
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1', port=3307,
                                   database='cna330')
    return conn

# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute("CREATE TABLE IF NOT EXISTS"
                   "JobHunter (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "Type VARCHAR(10)"
                   "Title VARCHAR(100)"
                   "Description TEXT CHARSET utf8"
                   "Job_ID VARCHAR(50)"
                   "Created_at DATE"
                   "Company VARCHAR(100)"
                   "Location VARCHAR(50)"
                   "How-to-apply VARCHAR(300))")
    return

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor

# Add a new job
def add_new_job(cursor, jobdetails):
    ## Add your code here
    type = jobdetails['Type']

    created_at = time.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y")

    company = jobdetails['Company']

    location = jobdetails['Location']

    title = jobdetails['Title']

    description = jobdetails['Description']

    how_to_apply = jobdetails['How_to_apply']

    job_id = jobdetails['id']

    query = cursor.execute(
        "INSERT INTO jobs(Type, Title, Description, Job_id, Created_at, Company, Location, How_to_apply" ") "

        "VALUES(?,?,?,?,?,?,?,?)", (type, title, description, job_id, created_at, company, location, how_to_apply))


    #query = "INSERT INTO JobHunter(Type, Title, Description, Job_ID, Created_at, Company, Location, How-to-apply)"
    #        "VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    return query_sql(cursor, query)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Add your code here
    query = "SELECT * FROM JobHunter WHERE Job_ID = \"%s\"" % job_id
    return query_sql(cursor, query)

def delete_job(cursor, jobdetails):
    ## Add your code here
    query = "DELETE FROM JobHunter WHERE Job_ID = \"%s\"" % job_id
    return query_sql(cursor, query)

# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?location=seattle"
    #query = "https://jobs.github.com/positions.json?" + "location=seattle" ## Add arguments here
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)
    except:
        pass
    return jsonpage

# Load a text-based configuration file

"""def load_config_file(filename):  

    argument_dictionary = 0

    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py

    rel_path = os.path.abspath(os.path.dirname(__file__))

    file = 0

    file_contents = 0

    try:

        file = open(filename, "r")

        file_contents = file.read()

    except FileNotFoundError:

        print("File not found, it will be created.")

        file = open(filename, "w")

        file.write("")

        file.close()



    ## Add in information for argument dictionary

    return argument_dictionary"""
#def load_config_file(filename):
#    argument_dictionary = 0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
#    rel_path = os.path.abspath(os.path.dirname(__file__))
#    file = 0
#    file_contents = 0
#    try:
#        file = open(filename, "r")
#        file_contents = file.read()
#    except FileNotFoundError:
#        print("File not found, it will be created.")
#        file = open(filename, "w")
#        file.write("")
#        file.close()

    ## Add in information for argument dictionary
#    return argument_dictionary

# Main area of the code.
def jobhunt(arg_dict):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)
    #print(jobpage[0])
    add_or_delete_job(jobpage, cursor)
    ## Add your code here to parse the job page
    #with urllib.request.urlopen("https://jobs.github.com/positions.json?location=seattle") as url:
    #    json_data = json.loads(url.read().decode())
    #    i = (json.dumps(json_data, indent=4, sort_keys=True))
    #    with open('jobdata.txt', "w") as f_file:
    #        f_file.write(i)  # Gabe help with this

    ## Add in your code here to check if the job already exists in the DB

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries
def add_or_delete_job(jobpage, cursor):

    # Add your code here to parse the job page

    for jobdetails in jobpage:  # EXTRACTS EACH JOB FROM THE JOB LIST

        # Add in your code here to check if the job already exists in the DB

        check_if_job_exists(cursor, jobdetails)

        is_job_found = len(cursor.fetchall()) > 0  # https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect

        if is_job_found:  # Help from Kevin Huynh

            # DELETE JOB

            # EXTRA CREDIT: Add your code to delete old entries

            now = datetime.now()

            job_date = datetime.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y")

            if (now - job_date).days > 30:  # https://stackoverflow.com/questions/46563442/check-if-dates-on-a-list-are-older-than-2-days

                print("Delete job: " + jobdetails["title"] + " from " + jobdetails["company"] + ", Created at: " + jobdetails["created_at"] + ", JobID: " + jobdetails['id'])

                delete_job(cursor, jobdetails)

        else:

            # INSERT JOB

            # Add in your code here to notify the user of a new posting

            print("New job is found: " + jobdetails["title"] + " from " + jobdetails["company"] + ", Created at: " + jobdetails["created_at"] + ", JobID: " + jobdetails['id'])

            add_new_job(cursor, jobdetails)
# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    #Load text file and store arguments into dictionary
    arg_dict = 0
    while(1):
        jobhunt(arg_dict)
        time.sleep(3600) # Sleep for 1h

if __name__ == '__main__':
    main()

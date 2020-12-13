import os
import sqlite3
from pprint import pprint
from googleapiclient import discovery
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# connect to sql database
con = sqlite3.connect('./History')

c = con.cursor()
c.execute("select title, url, visit_count from urls") #Change this to your prefered query (other vars: visit_count, last_visit_time from urls)
results = c.fetchall()

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('habittracker-36bda3a95231.json', scope)
# creds = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ananyapamal/Documents/ananya_grade9/HackTJ7.5/HabitTracker/client_secret.json"
client = gspread.authorize(creds)

sheet = client.open("habittracker").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# print webiste name, url, and number of times visited to spreadsheet
for i in range(0, 10, 1):
    sheet.update_cell(i + 2, 1, results[i][0])
    sheet.update_cell(i + 2, 2, results[i][1])
    sheet.update_cell(i + 2, 3, results[i][2])

# print out most used website and website name
maxVal = results[0][2]
maxWeb = None
for i in range(1, 10):
    if maxVal < results[i][2]:
        maxVal = results[i][2]
        maxWeb = results[i][0]
sheet.update_cell(15, 1, maxVal)
sheet.update_cell(15, 2, maxWeb)
    
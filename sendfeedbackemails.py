import gspread
from oauth2client.service_account import ServiceAccountCredentials

import smtplib
from email.message import EmailMessage

import time

# These are the websites that need to be accessed to get menteeData from Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

# Uses info from the JSON file and the scope to access Teagan's google drive
# This is stored in a variable (credentials)
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

# Uses the credentials variable to access google spreadsheets
gc = gspread.authorize(credentials)

menteeData = gc.open('Master Sheet').sheet1

mentorData = gc.open('Master Sheet').get_worksheet(1)

menteeEmailWKS = menteeData.col_values(2)

mentorEmailWKS = mentorData.col_values(2)

menteeEmails = menteeEmailWKS[1:]

mentorEmails = mentorEmailWKS[1:]


password = input("Please enter the password for coming2carleton@gmail.com: ")

def sendMenteeEmails(menteeEmails, password):

    for menteeEmail in menteeEmails:
        msg = EmailMessage()
        msg1 = "Hello"
        msg['Subject'] = 'hello'
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = menteeEmail
        msg.set_content(msg1)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("coming2carleton@gmail.com", password)
            smtp.send_message(msg)
            smtp.quit()

        time.sleep(1)
sendMenteeEmails(menteeEmails, password)

def sendMentorEmails(menteeEmails, password):

    for mentorEmail in mentorEmails:
        msg = EmailMessage()
        msg1 = "Hello"
        msg['Subject'] = 'hello'
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = mentorEmail
        msg.set_content(msg1)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("coming2carleton@gmail.com", password)
            smtp.send_message(msg)
            smtp.quit()

        time.sleep(1)
sendMentorEmails(mentorEmails, password)

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

allEmails = gc.open('Emails to send').sheet1

menteeEmailWKS = allEmails.col_values(1)

mentorEmailWKS = allEmails.col_values(2)

menteeEmails = menteeEmailWKS[1:]

mentorEmails = mentorEmailWKS[1:]


password = input("Please enter the password for coming2carleton@gmail.com: ")

def sendMenteeEmails(menteeEmails, password):

    for menteeEmail in menteeEmails:
        msg = EmailMessage()
        menteeMsg = "\nThank you for participating in the Coming2Carleton program! We hope you had a great experience."\
        +"\n\nWe'd love to hear about any feedback. Here is a link to fill out a short form! Please fill it out if possible; "
        + "We want to improve the program, and it really helps us out!"\
        +"\n\nhttps://forms.gle/cwZp37Jhrsnjb2LF7"\
        +"\n\nBest,\nThe Coming2Carleton team"
        msg['Subject'] = 'Coming2Carleton Feedback! (Incoming Students)'
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
        mentorMsg = "\nThank you for participating in the Coming2Carleton program! We hope you had a great experience."\
        +"\n\nWe'd love to hear about any feedback. Here is a link to fill out a short form! Please fill it out if possible; "
        + "We want to improve the program, and it really helps us out!"\
        +"\n\nhttps://forms.gle/cwZp37Jhrsnjb2LF7"\
        +"\n\nBest,\nThe Coming2Carleton team"
        msg['Subject'] = 'Coming2Carleton Feedback (Mentors)!'
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = mentorEmail
        msg.set_content(mentorMsg)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("coming2carleton@gmail.com", password)
            smtp.send_message(msg)
            smtp.quit()

        time.sleep(1)
sendMentorEmails(mentorEmails, password)

CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Uses
 * Requirements
 * Installation + Configuration
 * Troubleshooting


Introduction
------------
The Coming2Carleton program is a program that matches incoming students to current students using a weighted matchmaking algorithm. There are three main characteristics: academic interests, extracurricular activities, and background. Using these three characteristics, our program makes highly compatible matches!

Uses
------------
This program is made to match incoming students with current students. By relying on Google Forms and Google Sheets, this program is able to use data collected from many different students, and match them based on their compatibility. This program only works if there are more current students than incoming students.

Requirements
------------
This program requires the following Python modules:
  - gspread
  - oauth2client.service_account
  - operator
  - smtplib
  - email.message
  - time
  - datetime

Installation + Configuration
-------------
1. Using pip, install gspread and oauth2client
2. Make a Google service account (using link): https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
3. Go to this link to create service account: https://console.developers.google.com/apis/dashboard?project=coming2carleton2
4. Install the Google Sheets and Google Drive APIs
5. Download the JSON file with your credentials included
6. Use the email from the JSON file (service email) and share the Google Sheet you want to edit with the service email.

Troubleshooting
------------
If you are having trouble creating a Google service account, these two videos will help you:
  1. https://www.youtube.com/watch?v=7I2s81TsCnc
  2. https://www.youtube.com/watch?v=yPQ2Gk33b1U

If you are having trouble installing gspread and oauth2client, make sure you are installing them with this syntax: 
  pip install gspread
  pip install oauth2client
  AND MAKE SURE THAT YOU ARE INSTALLING THESE INTO YOUR REPOSITORY FOLDER

Any other questions, email: johnsont4@carleton.edu

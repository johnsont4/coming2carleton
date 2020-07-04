# feedbackdata.py stores feedback from participants on how the match worked out.
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# These are the websites that need to be accessed to get incomingData from Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

# Uses info from the JSON file and the scope to access Teagan's google drive
# This is stored in a variable (credentials)
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

# Uses the credentials variable to access google spreadsheets
gc = gspread.authorize(credentials)

# This is all the data for incoming students
inwks = gc.open('GoogleF').sheet1

# This is all the data for volunteer students
volwks = gc.open("GoogleF").get_worksheet(1)

#Spreadsheet with incoming data
indatasheet = gc.open("DataF").sheet1

#Spreadsheet with volunteer data
voldatasheet = gc.open("DataF").get_worksheet(1)

# These are lists of dictionaries that hold the variables for each group of students
incomingData = inwks.get_all_records()

volunteerData = volwks.get_all_records()



for inStudent in incomingData:
    inStudentValues = list(inStudent.values())
    indatasheet.append_row(inStudentValues)


for volStudent in volunteerData:
    volStudentValues = list(volStudent.values())
    voldatasheet.append_row(volStudentValues)









##

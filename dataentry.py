# feedbackdata.py stores feedback from participants on how the match worked out.
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from c2cdatabase import matches, mentees, mentors

from student import Student, Mentee, Mentor

# These are the websites that need to be accessed to get incomingData from Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

# Uses info from the JSON file and the scope to access Teagan's google drive
# This is stored in a variable (credentials)
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

# Uses the credentials variable to access google spreadsheets
gc = gspread.authorize(credentials)

#Spreadsheet with incoming data
menteedatasheet = gc.open("DataF").sheet1

#Spreadsheet with volunteer data
mentordatasheet = gc.open("DataF").get_worksheet(1)

#Spreadsheet with matches
matchesdatasheet = gc.open("DataF").get_worksheet(2)

#This function inputs the first sheet of DataF with each mentee object's attributes
def updateMenteeData():
    #This list will eventually contain a list of each mentee's attributes
    listOfMentees = []
    #This for loop appends each mentee's attributes to the listOfMentees in the form of a list
    for mentee in mentees:
        oneMentee = list(vars(mentees[mentee]).values())
        listOfMentees.append(oneMentee)

    #This for loop inserts each mentee list into the google sheet
    for mentee1 in listOfMentees:
        menteedatasheet.insert_row(mentee1, 2)
updateMenteeData()

#This function inputs the second sheet of DataF with each mentor object's attributes
def updateMentorData():
    #This list will eventually contain a list of each mentor's attributes
    listOfMentors = []
    #This for loop appends each mentor's attributes to the listOfMentors in the form of a list
    for mentor in mentors:
        oneMentor = list(vars(mentors[mentor]).values())
        listOfMentors.append(oneMentor)

    #This for loop inserts each mentor list into the google sheet
    for mentor1 in listOfMentors:
        mentordatasheet.insert_row(mentor1, 2)
updateMentorData()

#This function inputs the third sheet of DataF with each match
def updateMatchesData():
    #Creates a list that will eventually contain smaller lists with matches
    listOfMatches = []
    #Converts dictionary of matches into lists of matches and adds them to listOfMatches
    for match in matches:
        pair = []
        pair.append(match)
        pair.append(matches[match])
        listOfMatches.append(pair)

    #Updates google sheet with matches
    for match1 in listOfMatches:
        matchesdatasheet.insert_row(match1, 2)
updateMatchesData()















##

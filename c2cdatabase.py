# Access to Google Spreadsheats and GoogleDrive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Imports Student class containing each students' attributes
from student import Student

#Needed for dictionary commands
import operator
import time

# These are the websites that need to be accessed to get incomingData from Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

# Uses info from the JSON file and the scope to access Teagan's google drive
# This is stored in a variable (credentials)
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

# Uses the credentials variable to access google spreadsheets
gc = gspread.authorize(credentials)

inwks = gc.open('GoogleF').sheet1

volwks = gc.open("GoogleF").get_worksheet(1)

# This creates a list of all the incomingData on the spreadsheet
# Each element of the list is another list that contains each students' attributes
incomingData = inwks.get_all_records()

volunteerData = volwks.get_all_records()
#############################################################################

# Gets number of students who filled out the form
for index, students in enumerate(incomingData, start = 1):
    pass
numStudents = index

# Gets number of variables
for index, variables in enumerate(incomingData[0], start = 1):
    pass
numVariables = index

# A list that will hold Student objects
studentClassList = []

# A function that makes a Student object each time it is called
def makeStudent(listOfAtt):

    student = Student(listOfAtt)
    studentClassList.append(student)

def createStudentList2(incomingData):
    for attributes in incomingData:
        attributes = list(attributes.values())
        makeStudent(attributes)
    return studentClassList

# Adds a volStudent with their compatability with the incoming student into the incoming student's dictionary each time it is called.
def makePair(incomingStudent, volStudent, points, allPairs):
    allPairs['volunteer{}'.format(volStudent)] = points
    return allPairs

# Finds each incoming students best match by using the makePair() function above for every possible incomingStudent and volStudent combination
def findMatches(incomingStudents):

    for incomingStudent in range((len(incomingStudents))):

        # Each incoming student gets a dictionary
        # This dictionary has keys and values
        # The keys are the volunteers
        # The values are each volunteer's compatability with the incoming student
        allPairs = {}
        incomingPronouns = incomingStudents[incomingStudent].getPronouns()
        incomingStudy = incomingStudents[incomingStudent].getStudy()
        incomingDomOrInt = incomingStudents[incomingStudent].getDomOrInt()
        incomingState = incomingStudents[incomingStudent].getState()
        incomingActivities = incomingStudents[incomingStudent].getActivities()
        incomingRace = incomingStudents[incomingStudent].getRace()

        # This second for loop is the thing that iterates through the second set of incomingData
        # Right now, it's iterating through the same list as above
        # Later, this will be the volunteer student list
        # volStudent stands for volunteer student
        for volStudent in range((len(incomingStudents))):

            #sleep is used to avoid requests/second error

            points = 0

            volPronouns = incomingStudents[volStudent].getPronouns()
            volStudy = incomingStudents[volStudent].getStudy()
            volDomOrInt = incomingStudents[volStudent].getDomOrInt()
            volState = incomingStudents[volStudent].getState()
            volActivities = incomingStudents[volStudent].getActivities()
            volRace = incomingStudents[volStudent].getRace()

            # the following if statements increment the points of a pairing by checking similarities in answers
            if incomingPronouns == volPronouns:
                points = points + 3

            # need to write a function called compareInterests() that compares both students' areas of interest and spits out a
            '''
            if incomingStudy == volStudy:
                points = points + compareInterests(incomingStudents[incomingStudent], )
            '''
            if incomingDomOrInt == volDomOrInt:
                points = points + 3
            if incomingState == volState:
                points = points + 3
            if incomingActivities == volActivities:
                points = points + 3
            if incomingRace == volRace:
                points = points + 3

            # Creates the dictionary for the incoming student
            # Each key is one of the volunteers and each value is their
            #respective compatability
            makePair(incomingStudent + 1, volStudent + 1, points, allPairs)

        # Finds the volunteer with the highest compatability
        # The variable is the name of one of the volunteers in the dictionary
        bestmatch = max(allPairs.items(), key = operator.itemgetter(1))[0]

        print(incomingStudents[incomingStudent].getFirstName(), "'s top match is ", bestmatch, " with a total of ", \
        allPairs[bestmatch], " points! \nNow we have to email: ", \
        incomingStudents[incomingStudent].getEmail(), sep="")
        print('')

#The main function of the whole program
def main():
    # Creates a list of Student objects
    incomingStudents = createStudentList2(incomingData)

    # finds best match for each student and prints out results
    findMatches(incomingStudents)

main()

##

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


# A list that will hold Student objects
inStudentList = []
volStudentList = []

# A function that makes a Student object each time it is called
def makeStudent(listOfAtt):

    student = Student(listOfAtt)
    return student

def createInStudentList(data):
    for attributes in data:
        attributes = list(attributes.values())
        student = makeStudent(attributes)
        inStudentList.append(student)
    return inStudentList

def createVolStudentList(data):
    for attributes in data:
        attributes = list(attributes.values())
        student = makeStudent(attributes)
        volStudentList.append(student)
    return volStudentList

# Adds a volStudent with their compatability with the incoming student into the incoming student's dictionary each time it is called.
def makePair(volStudent, points, allPairs):
    allPairs[volStudent.getFirstName()] = points
    return allPairs

# Finds each incoming students best match by using the makePair() function above for every possible incomingStudent and volStudent combination
def findMatches(incomingStudents, volunteerStudents):

    for inStudent in incomingStudents:

        # Each incoming student gets a dictionary
        # This dictionary has keys and values
        # The keys are the volunteers
        # The values are each volunteer's compatability with the incoming student
        allPairs = {}
        inPronouns = inStudent.getPronouns()
        inStudy = inStudent.getStudy()
        inDomOrInt = inStudent.getDomOrInt()
        inState = inStudent.getState()
        inActivities = inStudent.getActivities()
        inRace = inStudent.getRace()

        # This second for loop is the thing that iterates through the second set of incomingData
        # Right now, it's iterating through the same list as above
        # Later, this will be the volunteer student list
        # volStudent stands for volunteer student
        for volStudent in volunteerStudents:

            #sleep is used to avoid requests/second error

            points = 0

            volPronouns = volStudent.getPronouns()
            volStudy = volStudent.getStudy()
            volDomOrInt = volStudent.getDomOrInt()
            volState = volStudent.getState()
            volActivities = volStudent.getActivities()
            volRace = volStudent.getRace()

            # the following if statements increment the points of a pairing by checking similarities in answers
            if inPronouns == volPronouns:
                points = points + 3

            # need to write a function called compareInterests() that compares both students' areas of interest and spits out a
            '''
            if inStudy == volStudy:
                points = points + compareInterests(incomingStudents[incomingStudent], )
            '''
            if inDomOrInt == volDomOrInt:
                points = points + 3
            if inState == volState:
                points = points + 1
            """if inActivities == volActivities:
                points = points + 3"""
            if inRace == volRace:
                points = points + 3

            # Creates the dictionary for the incoming student
            # Each key is one of the volunteers and each value is their
            #respective compatability
            makePair(volStudent, points, allPairs)

        # Finds the volunteer with the highest compatability
        # The variable is the object of one of the volunteers in the dictionary
        compatibleVolunteer = max(allPairs.items(), key = operator.itemgetter(1))[0]

        for volStudent in volunteerStudents:
            if volStudent.getFirstName() == compatibleVolunteer:
                compatibleVolunteer = volStudent

        print(inStudent.getFirstName(), " is compatible with ", compatibleVolunteer.getFirstName(), ". \
        \nTheir compatability score is: ", allPairs[compatibleVolunteer.getFirstName()], "\nNow, ", \
        compatibleVolunteer.getFirstName(), " has to email ", inStudent.getFirstName(), ". \n", inStudent.getFirstName(), \
        "'s email is: ", inStudent.getEmail(), ". \n", compatibleVolunteer.getFirstName(), "'s email is: ", \
        compatibleVolunteer.getEmail(), sep = "")

        print('')

#The main function of the whole program
def main():
    # Creates a list of Student objects

    incomingStudents = createInStudentList(incomingData)
    volunteerStudents = createVolStudentList(volunteerData)


    # finds best match for each student and prints out results
    findMatches(incomingStudents, volunteerStudents)

main()

##

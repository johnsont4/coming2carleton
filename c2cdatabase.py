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

# This is all the data for incoming students
inwks = gc.open('GoogleF').sheet1

# This is all the data for volunteer students
volwks = gc.open("GoogleF").get_worksheet(1)

# These are dictionaries that hold the variables for each group of students
incomingData = inwks.get_all_records()

volunteerData = volwks.get_all_records()
#############################################################################

# Two lists that will hold incoming students and volunteer students
inStudentList = []
volStudentList = []

# A function that makes a Student object each time it is called
def makeStudent(listOfAtt):
    student = Student(listOfAtt)
    return student

# This function creates all the incoming Student objects and adds them to inStudentList
def createInStudentList(data):
    for attributes in data:
        attributes = list(attributes.values())
        student = makeStudent(attributes)
        inStudentList.append(student)
    return inStudentList

# This function creates all the volunteer Students objects and adds them to volStudentList
def createVolStudentList(data):
    for attributes in data:
        attributes = list(attributes.values())
        student = makeStudent(attributes)
        volStudentList.append(student)
    return volStudentList

# Creates a new key-value pair in an incoming student's dictionary where the key is the volunteer student's name and the value is the compatability between them
def makePair(volStudent, points, allPairs):
    allPairs[volStudent.getFirstName()] = points
    return allPairs
def getCompatibility(inStudent, volStudent):
    inPronouns = inStudent.getPronouns()
    inStudy = inStudent.getStudy()
    inDomOrInt = inStudent.getDomOrInt()
    inState = inStudent.getState()
    inActivities = inStudent.getActivities()
    inRace = inStudent.getRace()

    volPronouns = volStudent.getPronouns()
    volStudy = volStudent.getStudy()
    volDomOrInt = volStudent.getDomOrInt()
    volState = volStudent.getState()
    volActivities = volStudent.getActivities()
    volRace = volStudent.getRace()

    points = 0

    # the following series of if-statements increment the points of a pairing by checking similarities in answers
    if inPronouns == volPronouns:
        points = points + 3

    # need to write a function called compareInterests() that compares both students' areas of interest and spits out a point total
    '''
    if inStudy == volStudy:
        points = points + compareInterests(incomingStudents[incomingStudent], )
    '''

    if inDomOrInt == volDomOrInt:
        points = points + 3
    if inState == volState:
        points = points + 1

    # need to write a function called compareActivities() that compares both students' activities and spits out a point total
    '''if inActivities == volActivities:
        points = points + 3'''

    if inRace == volRace:
        points = points + 3

    return points

# Finds each incoming student's best match by using the makePair() function above for every possible incomingStudent and volStudent combination and prints out the results
def findMatches(incomingStudents, volunteerStudents):

    # iterates through each incoming student
    # Does this by iterating through incomingStudents, a list holding incoming Student objects
    for inStudent in incomingStudents:

        # Each incoming student gets a dictionary: allPairs
        # This dictionary has keys and values
        # The keys are the volunteers
        # The values are each volunteer's compatability with the incoming student

        allPairs = {}

        # This second for-loop iterates through each volunteer student for every iteration of the outer loop
        # Every incoming student is compared with every volunteer student
        # iterates through volunteerStudents, a list holding volunteer Student objects

        for volStudent in volunteerStudents:

            compatibility = getCompatibility(inStudent, volStudent)

            # Creates a new key-value pair within an incoming student's dictionary as described earlier
            makePair(volStudent, compatibility, allPairs)

        # Finds the volunteer with the highest compatability
        # The variable is a string holding the first name of that volunteer
        compatibleVolunteer = max(allPairs.items(), key = operator.itemgetter(1))[0]

        # Converts from the volunteer's name to its object
        # Does this by iterating through volunteerStudents
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
    # Creates two lists of Student objects, one holding incoming students and one holding volunteer students

    incomingStudents = createInStudentList(incomingData)
    volunteerStudents = createVolStudentList(volunteerData)

    # finds best match for each incoming student and prints out results
    findMatches(incomingStudents, volunteerStudents)

main()

##

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

# A list that will hold incoming students
inStudentList = []

# A dictionary that will have volunteer names as keys and their respective Student object as keys
volStudentDict = {}

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

# This function creates all the volunteer Students objects and adds each key-value pair to the dictionary.
def createVolStudentList(data):
    for attributes in data:
        attributes = list(attributes.values())
        volStudent = makeStudent(attributes)
        volStudentDict[volStudent.getFirstName() + volStudent.getLastName()] = volStudent

    return volStudentDict

# Creates a new key-value pair in an incoming student's dictionary where the key is the volunteer student's name and the value is the compatability between them
def makePair(volStudent, points, allPairs):
    allPairs[volStudent.getFirstName() + volStudent.getLastName()] = points
    return allPairs

# Uses a series of if-statements and a couple methods to determine a number representing the compatibility between two students.
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

    points += 5 * inStudent.compareAttribute(volStudent, "study")
    points += 2 * inStudent.compareAttribute(volStudent, "activities")

    if inDomOrInt == volDomOrInt:
        points = points + 3

    if inState == volState:
        points = points + 2

    ###points = points + inStudent.compareStudy(volStudent)

    if inRace == volRace:
        points = points + 3

    return points

# Finds each incoming student's best match by using the makePair() function above for every possible incomingStudent and volStudent combination and prints out the results
def findMatches(incomingStudents, volunteerStudents):

    # Iterating through incomingStudents, a list holding incoming Student objects
    for inStudent in incomingStudents:

        # Each incoming student gets a dictionary, allPairs, which has keys(volunteer's name) and values(volunteer's compatability with the incoming student
        allPairs = {}

        # This second for-loop iterates through each volunteer student for every iteration of the outer loop
        # Every incoming student is compared with every volunteer student by iterating through the values of volunteerStudents,
        # a dictionary with keys = their first and last names, values = their respective Student obejct
        for volStudent in volunteerStudents.values():
            compatibility = getCompatibility(inStudent, volStudent)

            # Creates a new key-value pair within an incoming student's dictionary as described earlier
            makePair(volStudent, compatibility, allPairs)

        # Finds the volunteer with the highest compatability
        # The variable is a string holding the first name of that volunteer
        compatibleVolunteer = max(allPairs.items(), key = operator.itemgetter(1))[0]

        #uses volStudentDict to get the volunteer Student object by inputting their first name + their last  name.
        compatibleVolunteer = volStudentDict[compatibleVolunteer]

        print(inStudent.getFirstName(), " is compatible with ", compatibleVolunteer.getFirstName(), ". \
        \nTheir compatability score is: ", allPairs[compatibleVolunteer.getFirstName() + compatibleVolunteer.getLastName()], "\nNow, ", \
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

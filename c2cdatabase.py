# Access to Google Spreadsheats and GoogleDrive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Imports Student class containing each students' attributes
from student import Student

#Needed for dictionary commands
import operator

# these are used to send emails
import smtplib
from email.message import EmailMessage

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

# A dictionary that will have incoming students' names as keys and their respective Student object as values
inStudentDict = {}

# A dictionary that will have volunteer names as keys and their respective Student object as values
volStudentDict = {}

# A function that makes a Student object using a list of attributes each time it is called
def makeStudent(listOfAtt):
    student = Student(listOfAtt)
    return student

# This function creates all the incoming Student objects and adds each key-value pair to inStudentDict dictionary.
def createInStudentDict(data):
    for attributes in data:
        attributes = list(attributes.values())
        inStudent = makeStudent(attributes)
        inStudentDict[inStudent.getFirstName() + inStudent.getLastName()] = inStudent

    return inStudentDict

# This function creates all the volunteer Student objects and adds each key-value pair to the volStudentDict dictionary.
def createVolStudentDict(data):
    for attributes in data:
        attributes = list(attributes.values())
        volStudent = makeStudent(attributes)
        volStudentDict[volStudent.getFirstName() + volStudent.getLastName()] = volStudent

    return volStudentDict

# Creates a new key-value pair in an incoming student's dictionary where the key is the volunteer student's name and the value is their compatability
def makePair(volStudent, points, possiblePairs):
    possiblePairs[volStudent.getFirstName() + volStudent.getLastName()] = points
    return possiblePairs

# Uses a series of if-statements and a couple methods to return a number representing the compatibility between two students.
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

    if inPronouns == volPronouns:
        points = points + 3

    points += 5 * inStudent.compareAttribute(volStudent, "study")

    points += 2 * inStudent.compareAttribute(volStudent, "activities")

    if inDomOrInt == volDomOrInt:
        points = points + 3

    if inState == volState:
        points = points + 2

    if inRace == volRace:
        points = points + 3

    return points

#This function sends emails to all the incoming students and volunteers. matchesDict holds all the matches, and the two dictionaries are passed in
# so that we can input key values(combined first and last name) and get the corresponding Student objects(so we can get info like their email addresses).
def sendEmails(matchesDict, incomingStudentDict, volunteerStudentDict):

    # This loops through the keys of matchesDict, which are the combined first and last names of incoming students.
    for incomingStudentName in matchesDict:

        # get the Student objects associated with this pairing
        incomingStudent = incomingStudentDict[incomingStudentName]
        volStudent = volunteerStudentDict[matchesDict[incomingStudentName]]

        # gets both email addresses
        inStudentAddress = incomingStudent.getEmail()
        volStudentAddress = volStudent.getEmail()

    # email incoming students with a desired message
        msg = EmailMessage()
        msg['Subject'] = "Information for C2C 2021 :)"
        msg['From'] = "emailAddressWeHaveYetToMake@gmail.com"
        msg['To'] = inStudentAddress
        msg.set_content("Welcome to Carleton! . . . your mentor's name is " + volStudent.getFirstName() + " " \
        volStudent.getLastName() + " and their email is: " + volStudent.getEmail() + " and here's more info blah blah blah")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("emailAddressWeHaveYetToMake@gmail.com", "password")
            smtp.send_message(msg)
            smtp.quit()

    # email the volunteers with a desired message
        msg = EmailMessage()
        msg['Subject'] = "Information for C2C 2021 :)"
        msg['From'] = "emailAddressWeHaveYetToMake@gmail.com"
        msg['To'] = volStudentAddress
        msg.set_content("Thank you for signing up to be a mentor for this year's Coming2Carleton program . . . your mentee's name is " + \
        incomingStudent.getFirstName() + " " + incomingStudent.getLastName() + " and their email is: " + incomingStudent.getEmail() + " and here's more info ")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("emailAddressWeHaveYetToMake@gmail.com", "password")
            smtp.send_message(msg)
            smtp.quit()

#This function enters key data to a spreadsheet. Not yet implemented.
def enterData():
    pass

# Finds each incoming student's best match and puts into a dictionary called compatibleMatchesDict, where keys = incoming student's combined first + last name)
# and values = volunteer student's combined first + last name)
def findMatches(incomingStudents, volunteerStudents):
    compatibleMatchesDict = {}

    # Iterating through the values of incomingStudents, a dictionary with incoming students' combined first + last names as keys
    # and their respective Student objects as keys.
    for inStudent in incomingStudents.values():

        # Each incoming student gets a dictionary, possiblePairs, which has keys(volunteer's name) and values(volunteer's compatability with the incoming student
        possiblePairs = {}

        # This second for-loop iterates through each volunteer student for every iteration of the outer loop
        # Every incoming student is compared with every volunteer student by iterating through the values of volunteerStudents,
        # a dictionary with keys = combined first and last names, values = their respective Student object
        for volStudent in volunteerStudents.values():

            compatibility = getCompatibility(inStudent, volStudent)

            # Creates a new key-value pair within an incoming student's dictionary as described earlier
            makePair(volStudent, compatibility, possiblePairs)

        # Finds the volunteer with the highest compatability
        # The variable is a string that cholds the combined first name + last name of the compatible volunteer student
        compatibleVolunteer = max(possiblePairs.items(), key = operator.itemgetter(1))[0]

        # This adds a key(incoming student's combined first + last name) and a value(their compatible volunteer's combined first and last name)
        #to compatibleMatchesDict. After the outer loop is done running, this will contain all compatible matches.
        compatibleMatchesDict[inStudent.getFirstName() + inStudent.getLastName()] = compatibleVolunteer

        # commented out print statement for testing purposes
        '''
        print(inStudent.getFirstName(), " is compatible with ", volunteerStudents[compatibleVolunteer].getFirstName(), ". \
        \nTheir compatability score is: ", possiblePairs[compatibleVolunteer], "\nNow, ", \
        volunteerStudents[compatibleVolunteer].getFirstName(), " has to email ", inStudent.getFirstName(), ". \n", inStudent.getFirstName(), \
        "'s email is: ", inStudent.getEmail(), ". \n", volunteerStudents[compatibleVolunteer].getFirstName(), "'s email is: ", \
        volunteerStudents[compatibleVolunteer].getEmail(), sep = "")

        print('')
        '''
    return compatibleMatchesDict

# The main function of the whole program
# Basically, the main function creates 2 dicts: one for incoming and one for volunteer students
# Then, it uses the findMatches function to compare the two lists and find each incoming student's
# most compatible mentor and adds into a dictionary that holds the compatible matches.
def main():
    # Creates two dictionaries: one that will have incoming students' names as keys and their respective Student object as values
    # and one that will have volunteer names as keys and their respective Student object as values
    incomingStudents = createInStudentDict(incomingData)
    volunteerStudents = createVolStudentDict(volunteerData)

    # finds best match for each incoming student and stores it in a dictionary with keys(incoming student's combined first + last name)
    # and values(volunteer student's combined first + last name)
    matches = findMatches(incomingStudents, volunteerStudents)

    # sends emails to all students. Commented out for now
    # sendEmails(matches, incomingStudents, volunteerStudents)

    # enters data into a spreadsheet(?) so we can analyze it. Not yet implemented, so commented out for now.
    # enterData()

main()

##

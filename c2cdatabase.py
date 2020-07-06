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

# used to force program to wait before sending emails
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

# These are lists of dictionaries that hold the variables for each group of students
incomingData = inwks.get_all_records()

volunteerData = volwks.get_all_records()
#############################################################################

# A dictionary that will have incoming students' emails and their respective Student object as values
inStudentDict = {}

# A dictionary that will have volunteer emails as keys and their respective Student object as values
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
        inStudentDict[inStudent.getEmail()] = inStudent

    return inStudentDict

# This function creates all the volunteer Student objects and adds each key-value pair to the volStudentDict dictionary.
def createVolStudentDict(data):
    for attributes in data:
        attributes = list(attributes.values())
        volStudent = makeStudent(attributes)
        volStudentDict[volStudent.getEmail()] = volStudent

    return volStudentDict

# Creates a new key-value pair in an incoming student's dictionary where the key is the volunteer student's email and the value is their compatability
def makePair(volStudent, points, possiblePairs):
    possiblePairs[volStudent.getEmail()] = points
    return possiblePairs

# Uses a series of if-Homelandments and a couple methods to return a number representing the compatibility between two students.
def getCompatibility(inStudent, volStudent):

    inPronouns = inStudent.getPronouns()
    inDomOrInt = inStudent.getDomOrInt()
    inHomeland = inStudent.getHomeland().lower()
    inRace = inStudent.getRace()

    volPronouns = volStudent.getPronouns()
    volDomOrInt = volStudent.getDomOrInt()
    volHomeland = volStudent.getHomeland().lower()
    volRace = volStudent.getRace()

    points = 0

    if inPronouns == volPronouns:
        points += 3

    points += 5 * inStudent.compareAttribute(volStudent, "study")

    points += 2 * inStudent.compareAttribute(volStudent, "activities")

    if inDomOrInt == volDomOrInt == "Domestic":
        points += 3
        if inHomeland == volHomeland:
            points += 3

    if inDomOrInt == volDomOrInt == "International":
        points += 5
        if inHomeland == volHomeland:
            points += 3

    if inRace == volRace:
        points += 3

    return points

#This function sends emails to all the incoming students and volunteers. matchesDict holds all the matches, and the two dictionaries are passed in
# so that we can input key values(email addresses) and get the corresponding Student objects(so we can get info like their names).
def sendEmails(matchesDict, incomingStudentDict, volunteerStudentDict):

    # This makes one of us type in the password so the password isn't in the script
    password = input("The password for coming2carleton@gmail.com: ")

    # This loops through the keys of matchesDict, which are the combined first and last names of incoming students.
    for incomingStudentEmail in matchesDict:

        # gets the volunteer student email associated with this incoming student
        volStudentAddress = matchesDict[incomingStudentEmail]

        # get the Student objects associated with this pairing
        incomingStudent = incomingStudentDict[incomingStudentEmail]
        volStudent = volunteerStudentDict[volStudentAddress]

        menteeMsg = "Welcome to Carleton! We are so glad that you've chosen Carleton to be your next home. " \
        + "We have finished the matchmaking process for this cycle, and below is information about the student we have paired up with you and ways to contact them! \n\n" \
        + "Your mentor's name: " + volStudent.getFirstName() + " " + volStudent.getLastName() + "\n" \
        + "Email: " + volStudentAddress + "\n" \
        + "Pronouns: " + volStudent.getPronouns() + "\n" \
        + "Phone number: " + "we have to figure this out \n\n" \
        + "Have fun with this! Again, we would like to give you our most heartfelt welcome to Carleton and we hope to see you around on campus!"

        mentorMsg = "Thank you for signing up to be a mentor for this year's Coming2Carleton program! " \
        + "We have finished the matchmaking process for this cycle, and below is information about the student we have paired up with you and ways to contact them! \n\n" \
        + "Your mentee's name: " + incomingStudent.getFirstName() + " " + incomingStudent.getLastName() + "\n" \
        + "Email: " + incomingStudentEmail + "\n" \
        + "Pronouns: " + incomingStudent.getPronouns() + "\n" \
        + "Phone number: " + "we have to figure this out \n\n" \
        + "We have attached a pdf that contain some basic guidelines and tips about interacting with your mentee. They're pretty basic and meant to " \
        + "improve the experience for both of you. Again, thank you for participating and remembe to have fun with this!"

    # email incoming students with a desired message
        msg = EmailMessage()
        msg['Subject'] = "Information for C2C 2021 :)"
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = incomingStudentEmail
        msg.set_content(menteeMsg)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("coming2carleton@gmail.com", password)
            smtp.send_message(msg)

        # a line so that the program waits 2 seconds between sending email so hopefully Google doesn't flag as spam
        time.sleep(1)
    # email the volunteers with a desired message
        msg = EmailMessage()
        msg['Subject'] = "Information for C2C 2021 :)"
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = volStudentAddress
        msg.set_content(mentorMsg)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("coming2carleton@gmail.com", password)
            smtp.send_message(msg)
            smtp.quit()

#This function enters key data to a spreadsheet. Not yet implemented.
def enterData():
    pass

# Finds each incoming student's best match and puts into a dictionary called compatibleMatchesDict, where keys = incoming student's email address)
# and values = volunteer student's email address)
def findMatches(incomingStudents, volunteerStudents):
    compatibleMatchesDict = {}

    # Iterating through the values of incomingStudents, a dictionary with incoming students' email addresses
    # and their respective Student objects as keys.
    for inStudent in incomingStudents.values():

        # Each incoming student gets a dictionary, possiblePairs, which has keys(volunteer's email address and values(volunteer's compatability with the incoming student
        possiblePairs = {}

        # This second for-loop iterates through each volunteer student for every iteration of the outer loop
        # Every incoming student is compared with every volunteer student by iterating through the values of volunteerStudents,
        # a dictionary with keys = volunteer email address, values = their respective Student object
        for volStudent in volunteerStudents.values():

            compatibility = getCompatibility(inStudent, volStudent)

            # Creates a new key-value pair within an incoming student's dictionary as described earlier
            makePair(volStudent, compatibility, possiblePairs)

        # Finds the volunteer with the highest compatability
        # The variable is a string holding the email address of that volunteer
        compatibleVolunteerEmail = max(possiblePairs.items(), key = operator.itemgetter(1))[0]

        # This adds a key(incoming student's email) and a value(their compatible volunteer's email) to compatibleMatchesDict.
        # After the outer loop is done running, this will contain all compatible matches.
        compatibleMatchesDict[inStudent.getEmail()] = compatibleVolunteerEmail

    return compatibleMatchesDict

# The main function of the whole program
# Basically, the main function creates 2 dicts: one for incoming and one for volunteer students
# Then, it uses the findMatches function to compare the two lists and find each incoming student's
# most compatible mentor and adds into a dictionary that holds the compatible matches.
def main():
    # Creates two dictionaries: one that will have incoming student email addresses and their respective Student object as values
    # and one that will have volunteer email addresses and their respective Student object as values
    incomingStudents = createInStudentDict(incomingData)
    volunteerStudents = createVolStudentDict(volunteerData)

    # finds best match for each incoming student and stores it in a dictionary with keys(incoming student email address)
    # and values(volunteer student email address)
    matches = findMatches(incomingStudents, volunteerStudents)

    # sends emails to all mentors and mentees
    sendEmails(matches, incomingStudents, volunteerStudents)

    # enters data into a spreadsheet(?) so we can analyze it. Not yet implemented, so commented out for now.
    # enterData()

main()

##

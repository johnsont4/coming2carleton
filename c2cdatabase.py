# Access to Google Spreadsheats and GoogleDrive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Imports Student class containing each students' attributes
from student import Student, Mentor, Mentee

#Needed for dictionary commands
import operator

# these are used to send emails
import smtplib
from email.message import EmailMessage

# used to force program to wait before sending emails
import time

# used to make sure emails don't get cut (each email is unique)
import random

# These are the websites that need to be accessed to get menteeData from Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

# Uses info from the JSON file and the scope to access Teagan's google drive
# This is stored in a variable (credentials)
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

# Uses the credentials variable to access google spreadsheets
gc = gspread.authorize(credentials)

# This is all the data for incoming students
menteewks = gc.open('GoogleF').sheet1

# This is all the data for volunteer students
mentorwks = gc.open("GoogleF").get_worksheet(1)

# These are lists of dictionaries that hold the variables for each group of students
menteeData = menteewks.get_all_records()

mentorData = mentorwks.get_all_records()
#############################################################################

# A dictionary that will have incoming students' emails and their respective Student object as values
menteeDict = {}

# A dictionary that will have volunteer emails as keys and their respective Student object as values
mentorDict = {}

# A function that makes a Student object using a list of attributes each time it is called
def makeMentee(listOfAtt):

    mentee = Mentee(listOfAtt)
    return mentee

def makeMentor(listOfAtt):
    mentor = Mentor(listOfAtt)
    return mentor

# This function creates all the incoming Student objects and adds each key-value pair to menteeDict dictionary.
def createMenteeDict(data):
    for attributes in data:
        attributes = list(attributes.values())
        mentee = makeMentee(attributes)
        menteeDict[mentee.getEmail()] = mentee

    return menteeDict

# This function creates all the volunteer Student objects and adds each key-value pair to the mentorDict dictionary.
def createMentorDict(data):
    for attributes in data:
        attributes = list(attributes.values())
        mentor = makeMentor(attributes)
        mentorDict[mentor.getEmail()] = mentor

    return mentorDict

# Creates a new key-value pair in an incoming student's dictionary where the key is the volunteer student's email and the value is their compatability
def makePair(mentor, points, possiblePairs):
    possiblePairs[mentor.getEmail()] = points
    return possiblePairs

# Uses a series of if-Homelandments and a couple methods to return a number representing the compatibility between two students.
def getCompatibility(mentee, mentor):

    inPronouns = mentee.getPronouns()
    inDomOrInt = mentee.getDomOrInt()
    inHomeland = mentee.getHomeland().lower()
    inRace = mentee.getRace()

    mentorPronouns = mentor.getPronouns()
    mentorDomOrInt = mentor.getDomOrInt()
    mentorHomeland = mentor.getHomeland().lower()
    mentorRace = mentor.getRace()

    points = 0

    if inPronouns == mentorPronouns:
        points += 3

    points += 5 * mentee.compareAttribute(mentor, "study")

    points += 2 * mentee.compareAttribute(mentor, "activities")

    if inDomOrInt == mentorDomOrInt == "Domestic":
        points += 3
        if inHomeland == mentorHomeland:
            points += 3

    if inDomOrInt == mentorDomOrInt == "International":
        points += 5
        if inHomeland == mentorHomeland:
            points += 3

    if inRace == mentorRace:
        points += 3

    return points

#This function sends emails to all the incoming students and volunteers. matchesDict holds all the matches, and the two dictionaries are passed in
# so that we can input key values(email addresses) and get the corresponding Student objects(so we can get info like their names).
def sendEmails(matchesDict, mentees, mentors):

    # This makes one of us type in the password so the password isn't in the script
    password = input("The password for coming2carleton@gmail.com: ")

    # This loops through the keys of matchesDict, which are the combined first and last names of incoming students.
    for menteeEmail in matchesDict:

        # gets the volunteer student email associated with this incoming student
        mentorAddress = matchesDict[menteeEmail]

        # get the Student objects associated with this pairing
        mentee = mentees[menteeEmail]
        mentor = mentors[mentorAddress]

        menteeMsg = "#REF " + str(random.randint(1000,9999))\
        + "\nDear " + mentee.getFirstName() + ","\
        + "\nWelcome to Carleton! We are so glad that you've chosen Carleton to be your next home."\
        + "\n\nBased on your academic interests, your extracurricular activities, and other factors, you have been matched with a current Carleton student!"\
        + "\n\nBelow is some information about your Coming2Carleton mentor."\
        + "\n\nYour mentor's name: " + mentor.getFirstName() + " " + mentor.getLastName()\
        + "\nEmail: " + mentorAddress\
        + "\nPronouns: " + mentor.getPronouns()\
        + "\nPhone number: " + "we have to figure this out"\
        + "\n\nWe hope that through the Coming2Carleton program, you will be able to better prepare yourself for the transition to campus, make a meaningful connection with a current student, and most importantly have fun."\
        + "\n\nBest, the Coming2Carleton team"\
        + "\n\n#REF " + str(random.randint(1000,9999))

        mentorMsg = "#REF " + str(random.randint(1000,9999))\
        + "\n Dear " + mentor.getFirstName() + ","\
        + "\nThank you for signing up to be a mentor for this year's Coming2Carleton program!"\
        + "\n\nThe matchmaking process for this cycle has just completed. Based on your academic interests, extracurricular activities, and other factors, you've been matched with an incoming student!"\
        + "\n\nBelow is some information about your Coming2Carleton mentee."\
        + "\n\nYour mentee's name: " + mentee.getFirstName() + " " + mentee.getLastName()\
        + "\nEmail: " + menteeEmail\
        + "\nPronouns: " + mentee.getPronouns()\
        + "\nPhone number: " + "we have to figure this out"\
        + "\n\nThe goal of the Coming2Carleton program is to reassure incoming students and answer any questions they may have about campus. The most important part is to have fun and make a new connection!"\
        + "\n\nWe have attached a pdf that contain some basic guidelines and tips that can prepare you for your meeting with your mentee. Please glance at the possible questions to prepare yourself for the meeting. Have fun!"\
        + "\n\nBest, the Coming2Carleton team"\
        + "\n\n#REF " + str(random.randint(1000,9999))

    # email incoming students with a desired message
        msg = EmailMessage()
        msg['Subject'] = "Information for C2C 2021 :)"
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = menteeEmail
        msg.set_content(menteeMsg)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("coming2carleton@gmail.com", password)
            smtp.send_message(msg)

        # a line so that the program waits 1 second between sending email so hopefully Google doesn't flag as spam
        time.sleep(1)
    # email the volunteers with a desired message
        msg = EmailMessage()
        msg['Subject'] = "Information for C2C 2021 :)"
        msg['From'] = "coming2carleton@gmail.com"
        msg['To'] = mentorAddress
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
def findMatches(mentees, mentors):
    compatibleMatchesDict = {}

    # Iterating through the values of mentees, a dictionary with incoming students' email addresses
    # and their respective Student objects as keys.
    for mentee in mentees.values():

        # Each incoming student gets a dictionary, possiblePairs, which has keys(volunteer's email address and values(volunteer's compatability with the incoming student
        possiblePairs = {}

        # This second for-loop iterates through each volunteer student for every iteration of the outer loop
        # Every incoming student is compared with every volunteer student by iterating through the values of mentors,
        # a dictionary with keys = volunteer email address, values = their respective Student object
        for mentor in mentors.values():

            compatibility = getCompatibility(mentee, mentor)

            # Creates a new key-value pair within an incoming student's dictionary as described earlier
            makePair(mentor, compatibility, possiblePairs)

        # Finds the volunteer with the highest compatability
        # The variable is a string holding the email address of that volunteer
        compatibleMentorEmail = max(possiblePairs.items(), key = operator.itemgetter(1))[0]

        # This adds a key(incoming student's email) and a value(their compatible volunteer's email) to compatibleMatchesDict.
        # After the outer loop is done running, this will contain all compatible matches.
        compatibleMatchesDict[mentee.getEmail()] = compatibleMentorEmail

    return compatibleMatchesDict

# The main function of the whole program
# Basically, the main function creates 2 dicts: one for incoming and one for volunteer students
# Then, it uses the findMatches function to compare the two lists and find each incoming student's
# most compatible mentor and adds into a dictionary that holds the compatible matches.
def main():
    # Creates two dictionaries: one that will have incoming student email addresses and their respective Student object as values
    # and one that will have volunteer email addresses and their respective Student object as values
    mentees = createMenteeDict(menteeData)
    mentors = createMentorDict(mentorData)

    # finds best match for each incoming student and stores it in a dictionary with keys(incoming student email address)
    # and values(volunteer student email address)
    matches = findMatches(mentees, mentors)

    # sends emails to all mentors and mentees
    sendEmails(matches, mentees, mentors)

    # enters data into a spreadsheet(?) so we can analyze it. Not yet implemented, so commented out for now.
    # enterData()

main()

##

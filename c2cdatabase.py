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

#Spreadsheet with incoming data
menteedatasheet = gc.open("Master Sheet").sheet1

#Spreadsheet with volunteer data
mentordatasheet = gc.open("Master Sheet").get_worksheet(1)

#Spreadsheet with matches
matchesdatasheet = gc.open("Master Sheet").get_worksheet(2)
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

# Creates a new key-value pair in an incoming student's dictionary where the key is the volunteer student's email and the value is their compatibility
def makePair(mentor, totalPoints, possiblePairs):
    possiblePairs[mentor.getEmail()] = totalPoints
    return possiblePairs

# Uses a series of if-Homelandments and a couple methods to return a number representing the compatibility between two students.
def getCompatibility(mentee, mentor):

    menteePronouns = mentee.getPronouns()
    menteeDomOrInt = mentee.getDomOrInt()
    menteeHomeland = mentee.getHomeland().lower()
    menteeRace = mentee.getRace()
    menteePreference = mentee.getPreference()

    mentorPronouns = mentor.getPronouns()
    mentorDomOrInt = mentor.getDomOrInt()
    mentorHomeland = mentor.getHomeland().lower()
    mentorRace = mentor.getRace()

    academicPoints = 0
    extracurricularPoints = 0
    originPoints = 0

    academicPoints += 5 * mentee.compareAttribute(mentor, "study")
    extracurricularPoints += 3 * mentee.compareAttribute(mentor, "activities")

    if menteePronouns == mentorPronouns == "They/them/theirs":
        originPoints += 4

    if menteePronouns == mentorPronouns == "He/him/his":
        originPoints += 2

    if menteePronouns == mentorPronouns == "She/her/hers":
        originPoints += 2

    if menteeDomOrInt == mentorDomOrInt == "Domestic":
        originPoints += 2

        if menteeHomeland == mentorHomeland:
            originPoints += 2

    if menteeDomOrInt == mentorDomOrInt == "International":
        originPoints += 4

        if menteeHomeland == mentorHomeland:
            originPoints += 3

            if menteeRace == mentorRace:
                originPoints -= 3

    if menteeRace == mentorRace:
        originPoints += 3

    if menteePreference == "Academic Interests (I want my match to have similar academic interests as me)":
        academicPoints *= 2

    if menteePreference == "Extracurriculars (I want my match to be involved in similar activities as me)":
        extracurricularPoints *= 2

    if menteePreference == "Origin (I want my match to be demographically similar to me)":
        originPoints *= 2

    return academicPoints + extracurricularPoints + originPoints

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

def enterData(matches, mentees, mentors):
    def updateMenteeData():
        currentMenteeEmails = set(menteedatasheet.col_values(2))

        #This list will eventually contain a list of each mentee's attributes
        listOfMenteesToAdd = []

        #This for loop appends each mentee's attributes to the listOfMentees in the form of a list
        for mentee in mentees:
            #Need this conditional to avoid duplications
            if mentees[mentee].getEmail() not in currentMenteeEmails:
                oneMentee = list(vars(mentees[mentee]).values())
                listOfMenteesToAdd.append(oneMentee)

        #This for loop inserts each mentee list into the google sheet
        for mentee1 in listOfMenteesToAdd:
            menteedatasheet.insert_row(mentee1, 2)
    updateMenteeData()

    #This function inputs the second sheet of Master Sheet with each mentor object's attributes
    def updateMentorData():
        currentMentorEmails = set(mentordatasheet.col_values(2))

        #This list will eventually contain a list of each mentor's attributes
        listOfMentorsToAdd = []

        #This for loop appends each mentor's attributes to the listOfMentors in the form of a list
        for mentor in mentors:
            #Need this conditional to avoid duplications
            if mentors[mentor].getEmail() not in currentMentorEmails:
                oneMentor = list(vars(mentors[mentor]).values())
                listOfMentorsToAdd.append(oneMentor)

        #This for loop inserts each mentor list into the google sheet
        for mentor1 in listOfMentorsToAdd:
            mentordatasheet.insert_row(mentor1, 2)
    updateMentorData()

    #This function inputs the third sheet of Master Sheet with each match
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

# Finds each incoming student's best match and puts into a dictionary called compatibleMatchesDict, where keys = incoming student's email address)
# and values = volunteer student's email address)
def findMatches(mentees, mentors):
    compatibleMatchesDict = {}

    # Iterating through the values of mentees, a dictionary with incoming students' email addresses
    # and their respective Student objects as keys.
    for mentee in mentees.values():

        # Each incoming student gets a dictionary, possiblePairs, which has keys(volunteer's email address and values(volunteer's compatibility with the incoming student
        possiblePairs = {}

        # This second for-loop iterates through each volunteer student for every iteration of the outer loop
        # Every incoming student is compared with every volunteer student by iterating through the values of mentors,
        # a dictionary with keys = volunteer email address, values = their respective Student object
        for mentor in mentors.values():
            compatibility = getCompatibility(mentee, mentor)

            # Creates a new key-value pair within an incoming student's dictionary as described earlier
            makePair(mentor, compatibility, possiblePairs)

        #Updates compatibility scores for both the mentor and the mentee
        #The compScore is an instance variable in the student class
        compScore = max(possiblePairs.items())[1]
        mentee.updateComp(compScore)

        # Finds the volunteer with the highest compatibility
        # The variable is a string holding the email address of that volunteer
        compatibleMentorEmail = max(possiblePairs.items(), key = operator.itemgetter(1))[0]

        mentors[compatibleMentorEmail].updateComp(compScore)

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

    # enters data into a spreadsheet so we can analyze it
    enterData(matches, mentees, mentors)

main()

##

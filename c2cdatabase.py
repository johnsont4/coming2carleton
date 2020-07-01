#Access to Google Spreadsheats and GoogleDrive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Imports student class containing each students' attributes
from student import Student

#Needed for dictionary commands
import operator
import time

#These are the websites that need to be accessed to get data from Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

#Uses info from the JSON file and the scope to access Teagan's google drive
#This is stored in a variable (credentials)
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

#Uses the credentials variable to access google spreadsheets
gc = gspread.authorize(credentials)

wks = gc.open('GoogleF').sheet1

#This creates a list of all the data on the spreadsheet
#Each element of the list is another list that contains each students' attributes
data = wks.get_all_records()

#############################################################################

#Counts total number of students who filled out the form
for index, students in enumerate(data, start = 1):
    pass
print(index)
numStudents = index

#Counts total number of variables
for index, variables in enumerate(data[0], start = 1):
    pass
numVariables = index

#Makes a student using the student class
studentClassList = []
def makeStudent(listOfAtt):

    student = Student(listOfAtt)
    studentClassList.append(student)

#This function creates a list of the students
#Each element of the list is an object of the student class
def studentList(students, variables):
    for student in range(students):
        time.sleep(1)
        listOfAtt = []
        for variable in range(variables):
            #sleep is used to avoid requests/second error
            time.sleep(.5)
            #First value of the coordinate is the rows
            #Second value of the coordinate is the columns
            #Need to add 2 to the rows to make up for starting at 0 and
            #for having a "title row"
            #Need to add 1 to the columns to make up for starting at 0

            listOfAtt.append((wks.cell(int(student)+2, variable + 1).value))

        makeStudent(listOfAtt)
    return studentClassList

#This variable (incomingStudents) is a list of student objects
incomingStudents = studentList(numStudents, numVariables)

#Adds volunteers and their compatability to each incoming students dictionary
def makePair(incomingStudent, volStudent, points, allPairs):
    allPairs['volunteer{}'.format(volStudent)] = points
    return allPairs

#Finds each incoming students best match by using the makePair function above
#The for loops in this function allow one incoming student to be compared with all volunteers
def findMatches(incomingStudents):

    #incomingStudent stands for incoming student
    for incomingStudent in range((len(incomingStudents))):

        #Each incoming student gets a dictionary
        #This dictionary has keys and values
        #The keys are the volunteers
        #The values are each volunteers compatability with the incoming student
        allPairs = {}
        incomingPronouns = incomingStudents[incomingStudent].getPronouns()
        incomingActivities = incomingStudents[incomingStudent].getActivities()

        #This second for loop is the thing that iterates through the second set of data
        #Right now, it's iterating through the same list as above
        #Later, this will be the volunteer student list
        #volStudent stands for volunteer student
        for volStudent in range((len(incomingStudents))):

            #sleep is used to avoid requests/second error


            points = 0

            volPronouns = incomingStudents[volStudent].getPronouns()
            volActivities = incomingStudents[volStudent].getActivities()

            #If the incoming and volunteer students' pronouns are the same,
            #their compatability goes up by 5 points
            if incomingPronouns == volPronouns:
                points = points + 5

            #If the incoming and volunteer students' activities are the same,
            #their compatability goes up by 3 points
            if incomingActivities == volActivities:
                points = points + 3

            #Creates the dictionary for the incoming student
            #Each key is one of the volunteers and each value is their
            #respective compatability
            makePair(incomingStudent + 1, volStudent + 1, points, allPairs)

        #Finds the volunteer with the highest compatability
        #The variable is the name of one of the volunteers in the dictionary
        bestmatch = max(allPairs.items(), key = operator.itemgetter(1))[0]

        print("Incoming ", incomingStudent + 1, "'s top match is ", bestmatch, " with a total of ", \
        allPairs[bestmatch], " points! \nNow we have to email: ", \
        incomingStudents[incomingStudent].getEmail(), sep="")
        print('')

#The main function of the whole program
def main():
    #This variable (incomingStudents) is a list of student objects
    incomingStudents = studentList(numStudents, numVariables)

    #finds best match for each student and prints out results
    findMatches(incomingStudents)

main()

<<<<<<< HEAD
#test
=======

##
>>>>>>> 4f7e1126cc48552a2d8dd83800ae45c478e9974c

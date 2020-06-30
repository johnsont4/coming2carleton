#Access to Google Spreadsheats
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
credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

#Uses the credentials to access google spreadsheets
gc = gspread.authorize(credentials)

wks = gc.open('GoogleF').sheet1

#This creates a list of all the data on the spreadsheet
#Each element of the list is another list that contains each students' attributes
data = wks.get_all_records()

#############################################################################


#Counts total number of students who filled out the form
for index, students in enumerate(data, start = 1):
    pass
totalstudents = index

#Counts total number of variables
for index, variables in enumerate(data[0], start = 1):
    pass
totalvariables = index

#Makes students using the student class
studentclasslist = []
def makestudent(listofatt):

    student = Student(listofatt)
    studentclasslist.append(student)


#This function creates a list of the students
#Each element of the list is an object of the student class
def studentList(students, variables):
    for j in range(students):
        listofatt = []
        for k in range(variables):
            #First value of the coordinate is the rows
            #Second value of the coordinate is the columns
            #Need to add 2 to the rows to make up for starting at 0 and
            #for having a "title row"
            #Need to add 1 to the columns to make up for starting at 0

            listofatt.append((wks.cell(int(j)+2, k + 1).value))

        makestudent(listofatt)
    return studentclasslist

#This variable (incomingstudents) is a list of student objects
incomingstudents = studentList(totalstudents, totalvariables)




#Adds volunteers and their compatability to each incoming students dictionary
def makePairs(i,j,points, allPairs):
    allPairs['volunteer{}'.format(j)] = points
    return allPairs

#Finds each incoming students best match by using the makePairs function above
#The for loops in this function allow one incoming student to be compared with all volunteers
def findPoints():

    for i in range((len(incomingstudents))):

        #sleep is used to avoid requests/second error
        time.sleep(.25)

        #Each incoming student gets a dictionary
        #This dictionary has keys and values
        #The keys are the volunteers
        #The values are each volunteers compatability with the incoming student
        allPairs = {}
        inpronouns = incomingstudents[i].getPronouns()
        ininterest = incomingstudents[i].getInterests()

        #This second for loop is the thing that iterates through the second set of data
        #Right now, it's iterating through the same list as above
        #Later, this will be the volunteer student list
        for j in range((len(incomingstudents))):

            points = 0

            vpronouns = incomingstudents[j].getPronouns()
            vinterest = incomingstudents[j].getInterests()

            #If the incoming and volunteer students' pronouns are the same,
            #their compatability goes up by 5 points
            if inpronouns == vpronouns:
                points = points + 5
            else:
                pass

            #If the incoming and volunteer students' interests are the same,
            #their compatability goes up by 3 points
            if ininterest == vinterest:
                points = points + 3
            else:
                pass

            #Creates the dictionary for the incoming student
            #Each key is one of the volunteers and each value is their
            #respective compatability
            makePairs(i+1,j+1,points, allPairs)

        #Finds the volunteer with the highest compatability
        #The variable is the name of one of the volunteers in the dictionary
        bestmatch = max(allPairs.items(), key=operator.itemgetter(1))[0]

        print("Incoming ", i+1, "'s top match is ", bestmatch, " with a total of ", \
        allPairs[bestmatch], " points! \nNow we have to email: ", \
        incomingstudents[i].getEmail(), sep="")
        print('')
findPoints()










##

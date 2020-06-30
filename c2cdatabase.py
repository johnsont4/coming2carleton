
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from student import Student
import operator
import time

scope = ['https://www.googleapis.com/auth/spreadsheets', \
'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name\
('Coming2Carleton.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('GoogleF').sheet1

data = wks.get_all_records()

#############################################################################


#Counts total number of students who filled out the form
studentcount = 0
for i in data:
    studentcount = studentcount + 1
totalstudents = studentcount

#Counts total number of variables
variablecount = 0
for i in data[0]:
    variablecount = variablecount + 1
totalvariables = int(variablecount)

#Makes students using the student class
studentclasslist = []
def makestudent(listofatt):

    student = Student(listofatt)
    studentclasslist.append(student)

#Sorts data by columns
"""def sortbycolumn():
    #Prints timestamp
    for j in range(totalstudents):
        print(wks.cell(int(j)+1, 1).value)

    #Prints pronouns
    for j in range(totalstudents):
        print(wks.cell(int(j)+1, 2).value)

    #Prints interests
    for j in range(totalstudents):
        print(wks.cell(int(j)+1, 3).value)

    #Prints hometown
    for j in range(totalstudents):
        print(wks.cell(int(j)+1, 4).value)

    #Prints Email
    for j in range(totalstudents):
        print(wks.cell(int(j)+1, 5).value)"""
#sortbycolumn()

#Sorts data by rows (by students, so more helpful)
"""def sortbyrow(students, variables):
    individualstudents = []
    studentlist = []
    print(type(studentlist))
    for j in range(students):
        for k in range(variables):
            #First value of the coordinate is the rows
            #Second value of the coordinate is the columns
            #Need to add 2 to the rows to make up for starting at 0 and
            #for having a "title row"
            #Need to add 1 to the columns to make up for starting at 0

            individualstudents.append(wks.cell(int(j)+2, k + 1).value)
            print(individualstudents)
    studentlist = list(studentlist.append(individualstudents))
    print(studentlist)
    individualstudents = []"""

#sortbyrow(totalstudents, totalvariables)


"""def basicsortbyrow():
    for j in range(totalstudents):
        print("")
        print("Student #",j+1,":",sep='')
        for k in range(totalvariables):
            #First value of the coordinate is the rows
            #Second value of the coordinate is the columns
            #Need to add 2 to the rows to make up for starting at 0 and
            #for having a "title row"
            #Need to add 1 to the columns to make up for starting at 0

            print(wks.cell(int(j)+2, k + 1).value)"""

#basicsortbyrow()

def studenttest(students, variables):
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

incomingstudents = studenttest(totalstudents, totalvariables)

#print(incomingstudents)


def makePairs(i,j,points, allPairs):
    allPairs['volunteer{}'.format(j)] = points
    return allPairs

def findPoints():

    for i in range((len(incomingstudents))):
        allPairs = {}
        inpronouns = incomingstudents[i].getPronouns()
        ininterest = incomingstudents[i].getInterests()
        for j in range((len(incomingstudents))):

            #sleep is used to avoid requests/second error
            time.sleep(.25)

            points = 0
            vpronouns = incomingstudents[j].getPronouns()
            vinterest = incomingstudents[j].getInterests()

            if inpronouns == vpronouns:
                points = points + 5
            else:
                pass

            if ininterest == vinterest:
                points = points + 3
            else:
                pass

            x = makePairs(i+1,j+1,points, allPairs)
        pairpoints = allPairs.values()
        bestpair = max(allPairs.items(), key=operator.itemgetter(1))[0]

        print("Incoming ", i+1, "'s top match is ", bestpair, " with a total of ", \
        allPairs[bestpair], " points! \nNow we have to email: ", incomingstudents[i].getEmail(), sep="")
        print('')
findPoints()










##

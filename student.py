class Student():
    def __init__(self, listOfAtt):
        self.time = listOfAtt[0]
        self.email = listOfAtt[1]
        self.firstName = listOfAtt[2]
        self.lastName = listOfAtt[3]
        self.pronouns = listOfAtt[4]
        self.domOrInt = listOfAtt[5]
        self.homeland = listOfAtt[6]
        self.race = listOfAtt[7]
        self.study = listOfAtt[8]
        self.activities = listOfAtt[9]
        self.compatibility = 0
        self.academicComp = 0
        self.extracurricularComp =  0
        self.originComp = 0

    def getTime(self):
        return self.time

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def getPronouns(self):
        return self.pronouns

    def getStudy(self):
        return self.study

    def getDomOrInt(self):
        return self.domOrInt

    def getHomeland(self):
        return self.homeland

    def getActivities(self):
        return self.activities

    def getRace(self):
        return self.race

    def getEmail(self):
        return self.email

    def updateComp(self, compatibility):
        self.compatibility = int(compatibility)

    def getComp(self):
        return self.compatibility

    def updateAcademicComp(self, academicComp):
        self.academicComp = int(academicComp)

    def getAcademicComp(self):
        return self.academicComp

    def updateExtracurricularComp(self, extracurricularComp):
        self.extracurricularComp = int(extracurricularComp)

    def getExtracurricularComp(self):
        return self.extracurricularComp

    def updateOriginComp(self, originComp):
        self.originComp = int(originComp)

    def getOriginComp(self):
        return self.originComp

    def compareAttribute(self, otherStudent, attribute):
        # the conditional assigns the desired attribute to the variables
        # then, their bodies strip all white space from each string in the two lists
        if attribute == "study":
            selfStrippedList = [x.strip(' ') for x in self.getStudy().split(",")]
            otherStrippedList = [x.strip(' ') for x in otherStudent.getStudy().split(",")]

        elif attribute == "activities":
            selfStrippedList = [x.strip(' ') for x in self.getActivities().split(",")]
            otherStrippedList = [x.strip(' ') for x in otherStudent.getActivities().split(",")]

        # the following two lines convert the lists into sets: unordered collections of elements
        selfActivitiesSet = set(selfStrippedList)
        otherActivitiesSet = set(otherStrippedList)

        # use a set's built-in intersection function to find the number of intersections
        intersection = selfActivitiesSet.intersection(otherActivitiesSet)
        numIntersections = len(list(intersection))

        return numIntersections

class Mentee(Student):
    def __init__(self, listOfAtt):
        super().__init__(listOfAtt)
        self.questions = listOfAtt[10]
        if listOfAtt[11] == "Academic Interests (I want my match to have similar academic interests as me)":
            self.preference = 'Academic Interests'
        elif listOfAtt[11] == "Extracurriculars (I want my match to be involved in similar activities as me)":
            self.preference = 'Extracurriculars'
        elif listOfAtt[11] == "Origin (I want my match to be demographically similar to me)":
            self.preference = 'Origin'
        self.advertise = listOfAtt[12]

    def getQuestions(self):
        return self.questions

    def getAdvertise(self):
        return self.advertise

    def getPreference(self):
        return self.preference

class Mentor(Student):
    def __init__(self, listOfAtt):
        super().__init__(listOfAtt)
        self.year = listOfAtt[10]
        self.advertise = listOfAtt[11]
        self.matchStatus = 0

    def getAdvertise(self):
        return self.advertise

    def getMatched(self):
        return self.matchStatus

    def incrementMatchStatus(self):
        self.matchStatus += 1

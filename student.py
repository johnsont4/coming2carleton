class Student():
    def __init__(self, listOfAtt):
        time = listOfAtt[0]
        firstName = listOfAtt[1]
        lastName = listOfAtt[2]
        pronouns = listOfAtt[3]
        study = listOfAtt[4]
        domOrInt = listOfAtt[5]
        state = listOfAtt[6]
        activities = listOfAtt[7]
        race = listOfAtt[8]
        email = listOfAtt[9]

        self.time = time
        self.firstName = firstName
        self.lastName = lastName
        self.pronouns = pronouns
        self.study = study
        self.domOrInt = domOrInt
        self.state = state
        self.activities = activities
        self.race = race
        self.email = email

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

    def getState(self):
        return self.state

    def getActivities(self):
        return self.activities

    def getRace(self):
        return self.race

    def getEmail(self):
        return self.email

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
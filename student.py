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

    def compareActivities(self, otherStudent):
        # the following two lines strip all white space from each string in the two lists
        strippedList1 = [x.strip(' ') for x in self.getActivities().split(",")]
        strippedList2 = [x.strip(' ') for x in otherStudent.getActivities().split(",")]

        # the following two lines convert the lists into sets: unordered collections of elements
        activitiesSet1 = set(strippedList1)
        activitiesSet2 = set(strippedList2)

        # use a set's built-in intersection function to find the number of intersections
        intersection = activitiesSet1.intersection(activitiesSet2)
        numIntersections = len(list(intersection))

        #print("the number of intersecting activities between" , self.getFirstName(), " and ", otherStudent.getFirstName(), " is ", numIntersections)

        return numIntersections * 2

    def compareStudy(self, otherStudent):
        # the following two lines strip all white space from each string in the two lists
        strippedList1 = [x.strip(' ') for x in self.getStudy().split(",")]
        strippedList2 = [x.strip(' ') for x in otherStudent.getStudy().split(",")]

        # the following two lines convert the lists into sets: unordered collections of elements
        studySet1 = set(strippedList1)
        studySet2 = set(strippedList2)

        # use a set's built-in intersection function to find the number of intersections
        intersection = studySet1.intersection(studySet2)
        numIntersections = len(list(intersection))

        #print("the number of intersecting areas of study between" , self.getFirstName(), " and ", otherStudent.getFirstName(), " is ", numIntersections)

        return numIntersections * 5

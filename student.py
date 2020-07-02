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

        activitiesSet = set(self.getActivities().split(","))
        intersection = activitiesSet.intersection(otherStudent.getActivities().split(","))
        numIntersections = len(list(intersection))
        #print("the number of intersecting activities between" , self.getFirstName(), " and ", otherStudent.getFirstName(), " is ", numIntersections)
        return numIntersections

class Student():
    def __init__(self, listofatt):
        time = listofatt[0]
        firstName = listofatt[1]
        lastName = listofatt[2]
        pronouns = listofatt[3]
        study = listofatt[4]
        domOrInt = listofatt[5]
        state = listofatt[6]
        activities = listofatt[7]
        race = listofatt[8]
        email = listofatt[9]

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

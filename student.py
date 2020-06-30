class Student():
    def __init__(self, listofatt):
        time = listofatt[0]
        pronouns = listofatt[1]
        interests = listofatt[2]
        hometown = listofatt[3]
        email = listofatt[4]

        self.time = time
        self.pronouns = pronouns
        self.interests = interests
        self.hometown = hometown
        self.email = email

    def getTime(self):
        return self.time

    def getPronouns(self):
        return self.pronouns

    def getInterests(self):
        return self.interests

    def getHometown(self):
        return self.hometown

    def getEmail(self):
        return self.email

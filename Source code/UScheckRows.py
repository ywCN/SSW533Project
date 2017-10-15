import GenFxns as gen
from datetime import datetime

'''
This py file contains the checkRow functions our Project uses
Use these functions to check if a row violates a UserStory

These are separated from the 'Project' class in order to increase testability
'''

def checkRow_US02(row):
    birth = row[2]
    marriage = row[3]
    if not gen.date_before(birth, marriage):
        return False
    return True

def checkRow_US03(row):
    #for i in range(len(row)):
    #    print(row[i])
    if row[3] != "NA":
            birth = datetime.strptime(row[2], '%Y-%m-%d').date()
            death = datetime.strptime(row[3], '%Y-%m-%d').date()
            if birth > death:
                return False
    return True

def checkRow_US04(row):
    marry = row[2]
    divorce = row[3]
    if not gen.date_before(marry, divorce):
        return False
    return True

import GenFxns as gen
from datetime import datetime

'''
This py file contains the functions our Project uses to check UserStory Logic
Use these functions to check if a row violates a UserStory

These are separated from the 'Project' class in order to increase testability

Note: 'checkRow' functions are written for processes that check UserStory logic on a row x row basis
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

def checkSiblings_US15(siblingStr):
    #This function should be passed the sibling list given by the parent's queryinfo call
    #siblingstr should be queryinfo[4][0] <- for later reference
    siblingsArr = siblingStr.split(" ")
    if(len(siblingsArr) >= 15):
        return False
    return True

def checkMaleLastNames_US16(db, familyInfo):
    #Checks that the last name of each son matches the last name of the father
    #Note: checkMaleLastNames returns false if all last names match, and a string (that reads as true in python) of mismatched names
    for family in queryInfo:
            fatherID = family[0]
            maleFamilyMembers = family[1].split(" ")
            familyID = family[2]
            fatherLN = self.get_name(fatherID).split('/')[1]
            for son in maleFamilyMembers:
                sonLN = self.get_name(son).split('/')[1]
                if flag:
                    print("ERROR: US16: Not all male members of family {} have the same last name.".format(males[2]))

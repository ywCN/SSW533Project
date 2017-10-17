import GenFxns as gen
from datetime import datetime

'''
This py file contains the functions our Project uses to check UserStory Logic
Use these functions to check if a row violates a UserStory

These are separated from the 'Project' class in order to increase testability

Note: 'checkRow' functions are written for processes that check UserStory logic on a row x row basis
'''
#NOTE - the most basic tesable logic for US01 is in GenFxns as the date_before function
def checkRow_US01(row):
    #returns a list of errors
    #an empty list is the desired output of no errors being detected
    dates = [row[2], row[3], row[4], row[5]]
    errorList = []
    for date in dates:
        if (not gen.before_today(date)):
            errorStr = "ERROR: US01: {" + date + "} occurs after today {" + datetime.today().date()  + "} for { " + gen.combine_id_name(row[0], row[1]) +  "}"
            errorList.append(errorStr)
    return errorList    
    
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
    fatherID = familyInfo[0]
    maleFamilyMembers = familyInfo[1].split(" ")
    familyID = familyInfo[2]
    fatherLN = db.get_name(fatherID).split('/')[1]
    for son in maleFamilyMembers:
        sonLN = db.get_name(son).split('/')[1]
        if sonLN != fatherLN:
            return False
    return True
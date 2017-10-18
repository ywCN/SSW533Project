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

def checkDates_US09(death, birth, father = True):
    #print(death, birth, father)
    #print(gen.date_before(birth, death) )
    #print(not gen.dates_within(death, birth, 9, 'months'))
    if father == True:
        if gen.date_before(birth, death) and not gen.dates_within(death, birth, 9, 'months'):
            return False
    else:
        if gen.date_before(death, birth):
            return False
    #print(death, birth, father)
    #print(birth)
    return True

def checkFatherCase_US12(father_birth, birth):
    if gen.date_before(father_birth, birth) and not gen.dates_within(father_birth, birth, 80, 'years'):
        return False
    return True

def checkMotherCase_US12(mother_birth, birth):
    if gen.date_before(mother_birth, birth) and not gen.dates_within(mother_birth, birth, 60, 'years'):
       return False
    return True

def checkSiblingBirthdays_US13(birth_a, birth_b):
    if not gen.dates_within(birth_a, birth_b, 2, 'days') and gen.dates_within(birth_a, birth_b, 8, 'months'):
        return False
    return True

def checkMultBirths_US14(db, sib):
    counter = 0
    #print(sib)
    for i in range(len(sib) - 1):
        prev = db.get_birthday(sib[i])
        cur = db.get_birthday(sib[i + 1])
        if gen.dates_within(prev, cur, 1, 'days'):
            counter += 1
            if counter > 5:
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
    #print(familyInfo)
    for son in maleFamilyMembers:
        sonLN = db.get_name(son).split('/')[1]
        if sonLN != fatherLN:
            #print(sonLN)
            #print(fatherLN)
            return False
    return True

def checkMarriage_US10(birth_a, birth_b, marriage):
    if gen.date_before(birth_a, marriage) and gen.date_before(birth_b, marriage):
        if gen.dates_within(birth_a, marriage, 14, 'years') \
                or gen.dates_within(birth_b, marriage, 14, 'years'):
            return False
    #print(birth_a, birth_b, marriage)
    return True

def checkMarriedSiblings_US18(p1, p2, sibling_list):
    #returns true if siblings are married
    if p1 in sibling_list and p2 in sibling_list:
        #print(sibling_list)
        return True
    return False
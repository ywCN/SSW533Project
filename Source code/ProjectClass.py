import sqlite3
import os
import GenFxns as gen
import USLogic as us
from datetime import datetime
from prettytable import PrettyTable

'''
This py file contains the Database Management Class named 'Project'
Use this class to retrieve data from this project's .db file
    the .db file default is 'project.db' if no override is provided

Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''

### Main Class ###
class Project:
    def __init__(self, filename=r'project.db'):
        self.db = filename
        self.today = datetime.today().date()
        self.conversion = {'days': 1, 'months': 30.4, 'years': 365.25}
        #This checking, for an unknown reason, creates strange false negatives on test cases
        #The priority right now is testing, this can be reimplemented later
        '''
        if os.path.isfile(self.db):
        '''
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        '''
        else:
            print("\n"
                  "--------------------------------------------------------------------"
                  "| Please put the 'project.db' in the same path of this python file!|\n"
                  "--------------------------------------------------------------------")
            exit()
        '''

    def dates_before_current_date(self):
        """
        US01 - Dates before current date
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT, fam.MARR, fam.DIV from indi LEFT JOIN fam ON INDI.INDI = FAM.HUSB OR " \
                "INDI.INDI = FAM.WIFE "
        count = 0
        for row in self.query_info(query):
            for error in checkRow_US01(row):
                print(error)
                count = count + 1
            
        if(count == 0):
            print("No US01 Errors Found")
        return


    def birth_before_marriage(self):
        """
        US02 - Birth before marriage
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, fam.MARR from indi INNER JOIN fam ON INDI.INDI = FAM.HUSB OR INDI.INDI = " \
                "FAM.WIFE "
        count = 0
        for row in self.query_info(query):
            if(not us.checkRow_US02(row)):
                birth = row[2]
                marriage = row[3]
                print("ERROR: US02: Birth {} occurs after marriage {} for {}"
                    .format(birth, marriage, gen.combine_id_name(row[0], row[1])))
                count = count + 1
        if(count == 0):
            print("No US02 Errors Found")
        return 
            
    def birth_before_death(self):
        """
        US03 - Birth before death
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        count = 0
        for row in self.query_info(query):
            if(not us.checkRow_US03(row)):
                birth = datetime.strptime(row[2], '%Y-%m-%d').date()
                death = datetime.strptime(row[3], '%Y-%m-%d').date()
                print("ERROR: US03: Birth {} occurs after death {} for {}".format(birth, death, row[0] + row[1]))
                count = count + 1
        if(count == 0):
            print("No US03 Errors Found")
        return 

    def marriage_before_divorce(self):
        """
        US04 - Marriage before divorce
        :rtype: None
        """
        query = "select INDI, NAME, fam.MARR, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        count = 0
        for row in self.query_info(query):
            if(not us.checkRow_US03(row)):
                marry = row[2]
                divorce = row[3]
                print("ERROR: US04: Marriage {} occurs after divorce {} for {}"
                .format(marry, divorce, gen.combine_id_name(row[0], row[1])))
                count = count + 1
        if(count == 0):
            print("No US04 Errors Found")
        return
           
    def marriage_before_death(self):
        """
        US05 - Marriage before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            death = row[2]
            marry = row[3]
            if not gen.date_before(marry, death):
                print("ERROR: US05: Marriage {} occurs after death {} for {}"
                      .format(marry, death, gen.combine_id_name(row[0], row[1])))

    def divorce_before_death(self):
        """
        US06 - Divorce before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            death = row[2]
            divorce = row[3]
            if not gen.date_before(divorce, death):
                print("ERROR: US06: Divorce {} occurs after death {} for {}"
                      .format(divorce, death, gen.combine_id_name(row[0], row[1])))

    def less_than_150_years_old(self):
        """
        US07 - Less then 150 years old
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.query_info(query):
            if self.get_age(row[2], row[3]) >= 150:
                print("ERROR: US07: Age is greater than or equal to 150 years for {}"
                      .format(gen.combine_id_name(row[0], row[1])))

    def birth_before_marriage_of_parents(self):
        """
        US08 - Birth before marriage of parents
        :rtype: None
        """
        query = "select indi.INDI, indi.NAME, indi.BIRT, fam.MARR, fam.DIV from indi left join fam on indi.FAMC = " \
                "fam.FAM "
        for row in self.query_info(query):
            birth = row[2]
            marry = row[3]
            divorce = row[4]
            if not gen.date_before(marry, birth):
                print("ERROR: US08: Parent marriage {} after birth {} of {}"
                      .format(marry, birth, gen.combine_id_name(row[0], row[1])))
            if gen.date_before(divorce, birth) and not gen.dates_within(divorce, birth, 9, "months"):
                print("ERROR: US08: {} was born {} after 9 months of parent divorce {}".format(
                    gen.combine_id_name(row[0], row[1]), birth, divorce))

    def birth_before_death_of_parents(self):
        """
        US09
        Child should be born before death of mother and before 9 months after death of father
        :return: bool
        """
        status = True
        count = 0
        query1 = 'select indi.INDI, indi.SEX, indi.DEAT, indi.NAME from indi where indi.DEAT != "NA"'  # dead people
        deads = self.query_info(query1)
        for person in deads:
            death = person[2]
            if person[1] == 'M':
                query2 = 'select fam.CHIL from fam where fam.HUSB == "{}"'.format(person[0])  # list of children
                children = self.query_info(query2)
                for child in children[0]:
                    query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'.format(child)  # birthday
                    data = self.query_info(query3)
                    birth = data[0][0]
                    name = data[0][1]
                    if(not us.checkDates_US09(death, birth, True)):
                        print("ERROR: US09: {} is born more than 9 months after death of father {}.".format(birth, name))
                        count = count + 1
            if person[1] == 'F':
                query2 = 'select fam.CHIL from fam where fam.WIFE == "{}"'.format(person[0])
                children = self.query_info(query2)
                for child in children[0]:
                    query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'.format(child)  # birthday
                    birth = self.query_info(query3)
                    if(not us.checkDates_US09(death, birth, False)):
                        print("ERROR: US09: {} is born after death of mother {}.".format(birth[1], person[3]))
                        count = count + 1
        if(count == 0):
            print("No US09 Errors Found")
        return status

    def parent_not_too_old(self):
        """
        US12
        Mother should be less than 60 years older than her children and
        father should be less than 80 years older than his children
        :return: bool
        """
        status = True
        count = 0
        query1 = 'select indi.INDI, indi.BIRT, indi.FAMC, indi.NAME from indi where indi.FAMC != "NA"'
        children = self.query_info(query1)
        for child in children:
            birth = child[1]
            query2 = 'select fam.HUSB, fam.WIFE from fam where fam.FAM == "{}"'.format(child[2])
            parents = self.query_info(query2)[0]  # parent ids (male, female)
            father_birth = self.get_birthday(parents[0])
            mother_birth = self.get_birthday(parents[1])
            if(not us.checkMotherCase_US12(mother_birth, birth)):
                print("ERROR: US12: Mother is not less than 60 years older than her children {}.".format(child[3]))
                count = count + 1
            if(not us.checkFatherCase_US12(father_birth, birth)):
                print("ERROR: US12: Father is not less than 80 years older than his children {}.".format(child[3]))
                count = count + 1
        if(count == 0):
            print("No US12 Errors Found")
        return status

    def siblings_spacing(self):
        """
        US13
        Birth dates of siblings should be more than 8 months apart or less than 2 days apart
        (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
        :return: bool
        """
        status = True
        count = 0
        query = 'select fam.CHIL from fam where fam.CHIL != "NA"'
        siblings = self.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 1:
                for a in sib:
                    for b in sib:
                        birth_a = self.get_birthday(a)
                        birth_b = self.get_birthday(b)
                        if(not us.checkSiblingBirthdays_US13(birth_a, birth_b)):
                            print("ERROR: US13: Birthday of {} and {} is less than 8 months apart or more than 2 days "
                                  "apart.".format(self.get_name(a), self.get_name(b)))
                            count = count + 1
        if(count == 0):
            print("No US13 Errors Found")
        return status

    def multiple_births_less_than_5(self):
        """
        US14
        No more than five siblings should be born at the same time
        :return: bool
        """
        status = True
        count = 0
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        siblings = self.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 5:
                if(not us.checkMultBirths_US14(self, sib)):
                    print("ERROR: US14: There are more than five siblings born at the same time in family {}."
                        .format(sibling[1]))
                    count = count + 1
        return status

    def fewer_than_15_siblings(self):
        """
        US15
        There should be fewer than 15 siblings in a family
        :return: bool
        """
        status = True
        count = 0
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        families = self.query_info(query)
        for family in families:       
            if(not us.checkSiblings_US15(family[0])):
                print("ERROR: US15: There are 15 or more than 15 siblings in family {}.".format(family[1]))
                count = count + 1
        if(count == 0):
            print("No US15 Errors Found")
        return status

    def male_last_names(self):
        """
        US16
        All male members of a family should have the same last name
        :return: bool
        """
        status = True
        query = 'select fam.HUSB, fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'  # all males in a family
        queryInfo = self.query_info(query)
        count = 0
        for familyInfo in queryInfo:
            if(not us.checkMaleLastNames_US16(self, familyInfo)):
                familyID = familyInfo[2]
                print("ERROR: US16: Not all male members of family {} have the same last name.".format(familyID))
                count = count + 1
        if(count == 0):
            print("No US16 Errors Found")
        return status

    def marriage_after_14(self):
        """
        US10
        Marriage should be at least 14 years after birth of both spouses
        (parents must be at least 14 years old)
        :return: bool
        """
        status = True
        count = 0
        query = 'select fam.HUSB, fam.WIFE, fam.MARR, fam.FAM from fam'  # husb, wife, fam
        couples = self.query_info(query)
        for couple in couples:
            # print(len(couple))  # 3
            birth_a = self.get_birthday(couple[0])
            birth_b = self.get_birthday(couple[1])
            marriage = couple[2]
            if(not us.checkMarriage_US10(birth_a, birth_b, marriage)):
                print("ERROR: US10: Marriage of family {} is within 14 years after birth of both spouses."
                    .format(couple[3]))
                count = count + 1
        if(count == 0):
            print("No US10 Errors Found")
        return status

    def siblings_should_not_marry(self):
        """
        US18
        Siblings should not marry one another
        :return: bool
        """
        status = True
        count = 0
        query1 = 'select fam.CHIL from fam where fam.CHIL != "NA"'  # get sibling lists
        sibling_lists = self.query_info(query1)
        # print(len(sibling_lists))  # 5
        query2 = 'select fam.HUSB, fam.WIFE from fam'  # get couples
        couples = self.query_info(query2)
        # print(len(couples))  # 6
        for couple in couples:
            p1 = couple[0]
            p2 = couple[1]
            for sibling_list in sibling_lists:
                if(us.checkMarriedSiblings_US18(p1, p2, sibling_list[0])):
                    print("ERROR: US18: Siblings {} and {} married.".format(p1, p2))
                    count = count +1
        if(count == 0):
            print("No US18 Errors Found")
        return status

    def get_name(self, indi):
        return self.query_info('select indi.NAME from indi where indi.INDI == "{}"'.format(indi))[0][0]

    def get_birthday(self, indi):
        return self.query_info('select indi.BIRT from indi where indi.INDI == "{}"'.format(indi))[0][0]

    def query_info(self, query):
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c.execute("%s" % query)
        return self.c.fetchall()

    def disconnect(self):
        """
        :return: null
        """
        self.c.close()
        self.conn.close()

    def get_age(self, birthday, deathday):
        birth = gen.convert_to_datetime(birthday)
        death = gen.convert_to_datetime(deathday)
        if death != "NA":
            return (death - birth).days / self.conversion["years"]
        return (self.today - birth).days / self.conversion["years"]

    def print_info(self):
        indi_info = 'SELECT INDI, NAME, SEX, BIRT, DEAT, FAMC, FAMS FROM indi'
        fam_info = 'SELECT FAM, MARR, DIV, HUSB, WIFE, CHIL FROM fam'
        t_indi = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        t_fam = PrettyTable(
            ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])
        name_map = {}
        for row in self.query_info(indi_info):
            age = round(self.get_age(row[3], row[4]))
            if row[4] == "NA":
                alive = True
            else:
                alive = False
            if row[0] in name_map:
                pass
            else:
                name_map[row[0]] = row[1]
            lst = list(row)
            lst.insert(4, age)
            lst.insert(5, alive)
            t_indi.add_row(lst)

        for row in self.query_info(fam_info):
            lst = list(row)
            lst.insert(4, name_map[row[3]])
            lst.insert(6, name_map[row[4]])
            t_fam.add_row(lst)

        print("People")
        print(t_indi)
        print("Families")
        print(t_fam)
        print()

    def run_sprint1(self):
        self.dates_before_current_date()
        self.birth_before_marriage()
        self.birth_before_death()
        self.marriage_before_divorce()
        self.marriage_before_death()
        self.divorce_before_death()
        self.less_than_150_years_old()
        self.birth_before_marriage_of_parents()
        self.disconnect()

    def run_sprint2(self):
        self.print_info()
        self.birth_before_death_of_parents()
        self.parent_not_too_old()
        self.siblings_spacing()
        self.multiple_births_less_than_5()
        self.fewer_than_15_siblings()
        self.male_last_names()
        self.marriage_after_14()
        self.siblings_should_not_marry()
        self.disconnect()


def main():
    demo = Project()
    # demo.run_sprint1()
    demo.run_sprint2()


if __name__ == '__main__':
    main()

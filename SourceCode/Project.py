import sqlite3
import os
import unittest
from datetime import datetime
from prettytable import PrettyTable
from dateutil.relativedelta import relativedelta


class ProjectUtil:
    """
    This class contains all utility methods.
    """
    def __init__(self, db_name=r'project.db'):
        # dbName is now overridable and can be run on different Databases for testing
        self.db = db_name
        self.today = datetime.today().date()
        self.conversion = {'days': 1, 'months': 30.4, 'years': 365.25}
        if os.path.isfile(self.db):
            self.conn = sqlite3.connect(self.db)
            self.c = self.conn.cursor()
        else:
            print("\n"
                  "--------------------------------------------------------------------\n"
                  "| Please put the 'project.db' in the same path of this python file!|\n"
                  "--------------------------------------------------------------------")
            exit()

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

    @staticmethod
    def convert_to_datetime(date):
        """
        :param date: str
        :return: datatime type or str "NA"
        """
        try:
            res = datetime.strptime(date, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            res = "NA"
        return res

    @staticmethod
    def combine_id_name(indi, name):
        return indi + " " + name

    def dates_within(self, date1, date2, limit, unit):
        """
        check the interval between two dates
        :param date1: first date in '%Y-%m-%d' format
        :param date2: second date in '%Y-%m-%d' format
        :param limit: int
        :param unit: str in ('days', 'months', 'years')
        :return: bool
        """
        dt1 = self.convert_to_datetime(date1)
        dt2 = self.convert_to_datetime(date2)
        if dt1 == "NA" or dt2 == "NA":
            return True
        if unit not in self.conversion:
            raise Exception("No such unit")
        return (abs((dt1 - dt2).days) / self.conversion[unit]) <= limit

    def date_before(self, before, after):
        """
        before happens first
        after happens later
        :param before: the date should happen first
        :param after: the date should happen after
        :return: bool
        """
        dt1 = self.convert_to_datetime(before)
        dt2 = self.convert_to_datetime(after)
        if dt1 == "NA" or dt2 == "NA":
            return True
        return dt1 < dt2  # after should be greater than before

    def before_today(self, date):
        dt = self.convert_to_datetime(date)
        if dt == "NA":
            return True
        return dt < self.today

    def get_age(self, birthday, deathday):
        birth = self.convert_to_datetime(birthday)
        death = self.convert_to_datetime(deathday)
        if death != "NA":
            return (death - birth).days / self.conversion["years"]
        return (self.today - birth).days / self.conversion["years"]

    def get_indi_age2(self, indi):
        # alternative get_age call that gathers the individual's bith and death data
        # DOES NOT FACTOR IN DEATHS as it is meant to determine birthorder-based 'age'
        age = self.get_age(self.get_birthday(indi), "NA")
        return age

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


class Sprint1:
    """
    This class contains methods for sprint1.
    No test case is created.
    """
    def __init__(self):
        self.tool = ProjectUtil()  # get tools ready

    def dates_before_current_date(self):
        """
        US01 - Dates before current date
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT, fam.MARR, fam.DIV from indi LEFT JOIN fam ON INDI.INDI = FAM.HUSB OR " \
                "INDI.INDI = FAM.WIFE "

        for row in self.tool.query_info(query):
            dates = [row[2], row[3], row[4], row[5]]
            for date in dates:
                if not self.tool.before_today(date):
                    print("ERROR: US01: {} occurs after today {} for {}"
                          .format(date, self.tool.today, self.tool.combine_id_name(row[0], row[1])))

    def birth_before_marriage(self):
        """
        US02 - Birth before marriage
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, fam.MARR from indi INNER JOIN fam ON INDI.INDI = FAM.HUSB OR INDI.INDI = " \
                "FAM.WIFE "
        for row in self.tool.query_info(query):
            birth = row[2]
            marriage = row[3]
            if not self.tool.date_before(birth, marriage):
                print("ERROR: US02: Birth {} occurs after marriage {} for {}"
                      .format(birth, marriage, self.tool.combine_id_name(row[0], row[1])))

    def birth_before_death(self):
        """
        US03 - Birth before death
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.tool.query_info(query):
            birth = row[2]
            death = row[3]
            if not self.tool.date_before(birth, death):
                print("ERROR: US03: Birth {} occurs after death {} for {}"
                      .format(birth, death, self.tool.combine_id_name(row[0], row[1])))

    def marriage_before_divorce(self):
        """
        US04 - Marriage before divorce
        :rtype: None
        """
        query = "select INDI, NAME, fam.MARR, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        for row in self.tool.query_info(query):
            marry = row[2]
            divorce = row[3]
            if not self.tool.date_before(marry, divorce):
                print("ERROR: US04: Marriage {} occurs after divorce {} for {}"
                      .format(marry, divorce, self.tool.combine_id_name(row[0], row[1])))

    def marriage_before_death(self):
        """
        US05 - Marriage before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.tool.query_info(query):
            death = row[2]
            marry = row[3]
            if not self.tool.date_before(marry, death):
                print("ERROR: US05: Marriage {} occurs after death {} for {}"
                      .format(marry, death, self.tool.combine_id_name(row[0], row[1])))

    def divorce_before_death(self):
        """
        US06 - Divorce before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.tool.query_info(query):
            death = row[2]
            divorce = row[3]
            if not self.tool.date_before(divorce, death):
                print("ERROR: US06: Divorce {} occurs after death {} for {}"
                      .format(divorce, death, self.tool.combine_id_name(row[0], row[1])))

    def less_than_150_years_old(self):
        """
        US07 - Less then 150 years old
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.tool.query_info(query):
            if self.tool.get_age(row[2], row[3]) >= 150:
                print("ERROR: US07: Age is greater than or equal to 150 years for {}"
                      .format(self.tool.combine_id_name(row[0], row[1])))

    def birth_before_marriage_of_parents(self):
        """
        US08 - Birth before marriage of parents
        :rtype: None
        """
        query = "select indi.INDI, indi.NAME, indi.BIRT, fam.MARR, fam.DIV from indi left join fam on indi.FAMC = " \
                "fam.FAM "
        for row in self.tool.query_info(query):
            birth = row[2]
            marry = row[3]
            divorce = row[4]
            if not self.tool.date_before(marry, birth):
                print("ERROR: US08: Parent marriage {} after birth {} of {}"
                      .format(marry, birth, self.tool.combine_id_name(row[0], row[1])))
            if self.tool.date_before(divorce, birth) and not self.tool.dates_within(divorce, birth, 9, "months"):
                print("ERROR: US08: {} was born {} after 9 months of parent divorce {}"
                      .format(self.tool.combine_id_name(row[0], row[1]), birth, divorce))

    def run_sprint1(self):
        # self.tool.print_info()
        self.dates_before_current_date()
        self.birth_before_marriage()
        self.birth_before_death()
        self.marriage_before_divorce()
        self.marriage_before_death()
        self.divorce_before_death()
        self.less_than_150_years_old()
        self.birth_before_marriage_of_parents()
        # self.tool.disconnect()


class Sprint2:
    """
    This class contains methods for sprint2.
    All test cases are created.
    """
    def __init__(self):
        self.tool = ProjectUtil()  # get tools ready

    def birth_before_death_of_parents(self):
        """
        US09
        Child should be born before death of mother and before 9 months after death of father
        :return: bool
        """
        status = True
        query1 = 'select indi.INDI, indi.SEX, indi.DEAT, indi.NAME from indi where indi.DEAT != "NA"'  # dead people
        deads = self.tool.query_info(query1)
        try:
            for person in deads:
                death = person[2]
                if person[1] == 'M':
                    query2 = 'select fam.CHIL from fam where fam.HUSB == "{}"'.format(person[0])  # list of children
                    children = self.tool.query_info(query2)
                    for child in children[0]:
                        query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'\
                            .format(child)  # birthday
                        data = self.tool.query_info(query3)
                        birth = data[0][1]
                        name = data[0][1]
                        if self.tool.date_before(death, birth) and self.tool.dates_within(death, birth, 9, 'months'):
                            status = False
                            print("ERROR: US09: {} is born 9 months after death of father {}.".format(birth, name))
                if person[1] == 'F':
                    query2 = 'select fam.CHIL from fam where fam.WIFE == "{}"'.format(person[0])
                    children = self.tool.query_info(query2)
                    for child in children[0]:
                        query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'\
                            .format(child)  # birthday
                        birth = self.tool.query_info(query3)
                        if not self.tool.date_before(death, birth):
                            status = False
                            print("ERROR: US09: {} is born after death of mother {}.".format(birth[1], person[3]))
        except IndexError:
            pass  # caused by bad data, but not part of the US
        return status

    def parent_not_too_old(self):
        """
        US12
        Mother should be less than 60 years older than her children and
        father should be less than 80 years older than his children
        :return: bool
        """
        status = True
        query1 = 'select indi.INDI, indi.BIRT, indi.FAMC, indi.NAME from indi where indi.FAMC != "NA"'
        children = self.tool.query_info(query1)
        for child in children:
            birth = child[1]
            query2 = 'select fam.HUSB, fam.WIFE from fam where fam.FAM == "{}"'.format(child[2])
            parents = self.tool.query_info(query2)[0]  # parent ids (male, female)
            father_birth = self.tool.get_birthday(parents[0])
            mother_birth = self.tool.get_birthday(parents[1])
            if self.tool.date_before(mother_birth, birth) \
                    and not self.tool.dates_within(mother_birth, birth, 60, 'years'):
                status = False
                print("ERROR: US12: Mother is not less than 60 years older than her children {}.".format(child[3]))
            if self.tool.date_before(father_birth, birth) \
                    and not self.tool.dates_within(father_birth, birth, 80, 'years'):
                status = False
                print("ERROR: US12: Father is not less than 80 years older than his children {}.".format(child[3]))

        return status

    def siblings_spacing(self):
        """
        US13
        Birth dates of siblings should be more than 8 months apart or less than 2 days apart
        (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
        :return: bool
        """
        status = True
        query = 'select fam.CHIL from fam where fam.CHIL != "NA"'
        siblings = self.tool.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 1:
                for a in sib:
                    for b in sib:
                        birth_a = self.tool.get_birthday(a)
                        birth_b = self.tool.get_birthday(b)
                        if not self.tool.dates_within(birth_a, birth_b, 2, 'days') \
                                and self.tool.dates_within(birth_a, birth_b, 8, 'months'):
                            status = False
                            print("ERROR: US13: Birthday of {} and {} is less than 8 months apart or more than 2 days "
                                  "apart.".format(self.tool.get_name(a), self.tool.get_name(b)))
        return status

    def multiple_births_less_than_5(self):
        """
        US14
        No more than five siblings should be born at the same time
        :return: bool
        """
        status = True
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        siblings = self.tool.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 5:
                counter = 0
                for i in range(len(sib) - 1):
                    prev = self.tool.get_birthday(sib[i])
                    cur = self.tool.get_birthday(sib[i + 1])
                    if self.tool.dates_within(prev, cur, 1, 'days'):
                        counter += 1
                        if counter > 5:
                            status = False
                            print("ERROR: US14: There are more than five siblings born at the same time in family {}."
                                  .format(sibling[1]))
                            break
        return status

    def fewer_than_15_siblings(self):
        """
        US15
        There should be fewer than 15 siblings in a family
        :return: bool
        """
        status = True
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        siblings = self.tool.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) >= 15:
                status = False
                print("ERROR: US15: There are 15 or more than 15 siblings in family {}.".format(sibling[1]))
                break
        return status

    def male_last_names(self):
        """
        US16
        All male members of a family should have the same last name
        :return: bool
        """
        status = True
        query = 'select fam.HUSB, fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'  # all males in a family
        males_fam = self.tool.query_info(query)
        for males in males_fam:
            ids = (males[0] + " " + males[1]).split()
            flag = False
            for a in ids:
                for b in ids:
                    name_a = self.tool.get_name(a).split('/')[1]
                    name_b = self.tool.get_name(b).split('/')[1]
                    if name_a != name_b:
                        flag = True
                        status = False
                        break
            if flag:
                print("ERROR: US16: Not all male members of family {} have the same last name.".format(males[2]))

        return status

    def marriage_after_14(self):
        """
        US10
        Marriage should be at least 14 years after birth of both spouses
        (parents must be at least 14 years old)
        :return: bool
        """
        status = True
        query = 'select fam.HUSB, fam.WIFE, fam.MARR, fam.FAM from fam'  # husb, wife, fam
        couples = self.tool.query_info(query)
        for couple in couples:
            birth_a = self.tool.get_birthday(couple[0])
            birth_b = self.tool.get_birthday(couple[1])
            marriage = couple[2]
            if self.tool.date_before(birth_a, marriage) and self.tool.date_before(birth_b, marriage):
                if self.tool.dates_within(birth_a, marriage, 14, 'years') \
                        or self.tool.dates_within(birth_b, marriage, 14, 'years'):
                    status = False
                    print("ERROR: US10: Marriage of family {} is within 14 years after birth of both spouses."
                          .format(couple[3]))
        return status

    def siblings_should_not_marry(self):
        """
        US18
        Siblings should not marry one another
        :return: bool
        """
        status = True
        query1 = 'select fam.CHIL from fam where fam.CHIL != "NA"'  # get sibling lists
        sibling_lists = self.tool.query_info(query1)
        query2 = 'select fam.HUSB, fam.WIFE from fam'  # get couples
        couples = self.tool.query_info(query2)
        for couple in couples:
            p1 = couple[0]
            p2 = couple[1]
            for sibling_list in sibling_lists:
                if p1 in sibling_list[0] and p2 in sibling_list[0]:
                    status = False
                    print("ERROR: US18: Siblings {} and {} married.".format(p1, p2))

        return status

    def run_sprint2(self):
        # self.tool.print_info()
        self.birth_before_death_of_parents()  # test case will run the method
        self.parent_not_too_old()
        self.siblings_spacing()
        self.multiple_births_less_than_5()
        self.fewer_than_15_siblings()
        self.male_last_names()
        self.marriage_after_14()
        self.siblings_should_not_marry()
        # self.tool.disconnect()


class TestSprint2(unittest.TestCase):
    """
    Unittest for Sprint 2.
    """

    def setUp(self):
        self.test = Sprint2()

    def test_birth_before_death_of_parents(self):
        self.assertFalse(self.test.birth_before_death_of_parents())

    def test_parent_not_too_old(self):
        self.assertFalse(self.test.parent_not_too_old())

    def test_siblings_spacing(self):
        self.assertFalse(self.test.siblings_spacing())

    def test_multiple_births_less_than_5(self):
        self.assertFalse(self.test.multiple_births_less_than_5())

    def test_fewer_than_15_siblings(self):
        self.assertFalse(self.test.fewer_than_15_siblings())

    def test_male_last_names(self):
        self.assertFalse(self.test.male_last_names())

    def test_marriage_after_14(self):
        self.assertFalse(self.test.marriage_after_14())

    def test_siblings_should_not_marry(self):
        self.assertFalse(self.test.siblings_should_not_marry())


class Sprint3:
    """
    This class contains methods for sprint3.
    All test cases are created.
    """
    def __init__(self):
        self.tool = ProjectUtil()  # get tools ready

    def unique_name_and_birth_date(self):
        """
        US23 (ALLA)
        Each individual has to have a unique name and birth date in GEDCOM file
        """
        status = True
        query = 'select NAME, BIRT from indi group by NAME, BIRT having COUNT(*) > 1'
        new_birth = self.tool.query_info(query)
        dup_name = new_birth[0][0]
        dup_birt = new_birth[0][1]
        if len(dup_name) > 3:
            status = False
            print("ERROR: US23: More than one individual has the name {} and birthday {}.".format(dup_name, dup_birt))
        return status

    def correct_gender_for_role(self):
        """
        US21 (ALLA)
        The husbands have to be male and wives have to be female
        """
        status = True
        query = 'select HUSB, WIFE from fam'
        couples = self.tool.query_info(query)
        for couple in couples:
            husband = self.tool.query_info('select INDI, NAME, SEX from indi where INDI == "{}"'.format(couple[0]))[0]
            wife = self.tool.query_info('select INDI, NAME, SEX from indi where INDI == "{}"'.format(couple[1]))[0]
            if husband[2] != 'M':
                status = False
                print("ERROR: US21: Husband {} {} is not male.".format(husband[0], husband[1]))
            if wife[2] != 'F':
                status = False
                print("ERROR: US21: Wife {} {} is not female.".format(wife[0], wife[1]))
        return status

    def unique_ids(self):
        """
        US22 All individual IDs should be unique and all family IDs should be unique
        author: Mutni
        :return: bool
        """
        status = True
        query1 = 'select INDI from indi group by INDI having COUNT(*) > 1'
        query2 = 'select FAM from fam group by FAM having COUNT(*) > 1'
        indi_id = self.tool.query_info(query1)
        fam_id = self.tool.query_info(query2)
        if len(indi_id) > 0:
            status = False
            print("ERROR: US22: Individual ID {} is not unique.".format(indi_id[0][0]))
        if len(fam_id) > 0:
            status = False
            print("ERROR: US22: Family ID {} is not unique.".format(fam_id[0][0]))
        return status

    def unique_first_names_in_families(self):
        """
        US25 No more than one child with the same name and birth date should appear in a family
        author: Mutni
        :return: bool
        """
        status = True
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        siblings = self.tool.query_info(query)
        dups = set()
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 1:
                for a in sib:
                    for b in sib:
                        if a != b:
                            name_a = self.tool.get_name(a)
                            birth_a = self.tool.get_birthday(a)
                            name_b = self.tool.get_name(b)
                            birth_b = self.tool.get_birthday(b)
                            if name_a == name_b and birth_a == birth_b:
                                dups.add((name_a, birth_a, sibling[1]))
        if len(dups) != 0:
            status = False
            for dup in dups:
                print("ERROR: US25: More than one child with the same name {} and birth date {} in family {}."
                      .format(dup[0], dup[1], dup[2]))
        return status

    def include_individual_ages(self):
        """
        US27
        author: Robyn
        :return: bool
        """
        status = True
        individuals = self.tool.query_info('select INDI, NAME, BIRT, DEAT from indi')
        if len(individuals) != 0:
            status = False
            for individual in individuals:
                trunc_age = int(self.tool.get_age(individual[2], individual[3]))
                if individual[3] != "NA":
                    print("US27: Individual with ID = {} was named {} and died at Age {}."
                          .format(individual[0], individual[1], trunc_age))
                else:
                    print("US27: Individual with ID = {} is named {} and is Aged {}."
                          .format(individual[0], individual[1], trunc_age))
        return status

    def order_siblings_by_age(self):
        # returns false when it detects siblings
        # this is the most useful use of a boolean output for this function
        """
        US28 prints individuals
        author: Robyn
        :return: bool
        """
        status = True
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        families = self.tool.query_info(query)
        # print ("US:28 SIBLINGS TEST" )
        for family in families:
            sib_dict = {}
            siblings = family[0].split(" ")
            twins_count = 1
            sib_string = ""
            for sibling in siblings:
                status = False
                sib_age = self.tool.get_indi_age2(sibling)
                # If there are twins, they will be listed in order they appear in the table
                # This is done by subtracting .0000001 from each subsequent twin's age
                if sib_age in sib_dict:
                    sib_age = sib_age - (.0000001 * twins_count)
                    twins_count = twins_count + 1
                sib_dict[sib_age] = sibling
            for key in sib_dict:
                if sib_string == "":
                    sib_string = sib_dict[key]
                else:
                    sib_string = sib_string + ", " + sib_dict[key]
            print("US28: The siblings, by birth order, in family " + family[1] + " are " + sib_string)
        return status

    def list_deceased(self):
        """
        US29
        author: Youhao
        :return: bool
        """
        status = True  # note: expected to return True for successfully displaying all deceased
        deads = self.tool.query_info('select INDI, NAME, DEAT from indi where DEAT != "NA"')
        if len(deads) != 0:
            status = False
            for dead in deads:
                print("US29: Found deceased person {} {} who died on {}.".format(dead[0], dead[1], dead[2]))
        return status

    def list_living_married(self):
        """
        US30
        author: Youhao
        :return: bool
        """
        status = True
        living_marries = self.tool.query_info('select INDI, NAME from indi where DEAT == "NA" and FAMS != "NA"')
        if len(living_marries) != 0:
            status = False
            for person in living_marries:
                print("US30: Found living married person {} {}.".format(person[0], person[1]))
        return status


class TestSprint3(unittest.TestCase):
    """
    Unittest for Sprint 3.
    """
                  
    def setUp(self):
        self.test = Sprint3()

    def test_unique_name_and_birth_date(self):
        self.assertFalse(self.test.unique_name_and_birth_date())

    def test_correct_gender_for_role(self):
        self.assertFalse(self.test.correct_gender_for_role())
        
    def test_unique_ids(self):
        self.assertFalse(self.test.unique_ids())

    def test_unique_first_names_in_families(self):
        self.assertFalse(self.test.unique_first_names_in_families())

    def test_include_individual_ages(self):
        self.assertFalse(self.test.include_individual_ages())

    def test_order_siblings_by_age(self):
        self.assertFalse(self.test.order_siblings_by_age())

    def test_list_deceased(self):
        self.assertFalse(self.test.list_deceased())

    def test_list_living_married(self):
        self.assertFalse(self.test.list_living_married())


class Sprint4:
    """
    This class contains methods for sprint4.
    All test cases are created.
    """
    def __init__(self):
        self.tool = ProjectUtil()  # get tools ready

    def list_living_single(self):
        """
        US31 (ALLA)
        List all living people over 30 who have never been married in a GEDCOM file
        """
        status = True
        living_singles = self.tool.query_info(
            'select INDI, NAME, BIRT, DEAT from indi where DEAT == "NA" and FAMS == "NA"')
        for single in living_singles:
            if self.tool.get_age(single[2], single[3]) > 30:
                status = False
                print("US31: Found living single person {} {}.".format(single[0], single[1]))
        return status
        
    def list_multiple_births(self):
        """
        US32 (ALLA)
        List all multiple births in a GEDCOM file
        """
        status = True
        query = 'select CHIL, FAM from fam where fam.CHIL != "NA"'
        siblings = self.tool.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 1:
                status = False
                print("US32: There are multiple births in the family {}.".format(sibling[1]))
        return status
    
    def list_orphans(self):
        """
        Author: Mutni
        US33 List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
        :return:
        """
        status = True
        people = self.tool.query_info('select INDI, BIRT, DEAT, FAMC, NAME from indi')
        for person in people:
            if self.tool.get_age(person[1], person[2]) < 18:
                parent = self.tool.query_info('select HUSB, WIFE from fam where FAM == "{}"'.format(person[3]))
                if len(parent) > 0:
                    alive1 = self.tool.query_info('select DEAT from indi where INDI == "{}"'.format(parent[0][0]))
                    alive2 = self.tool.query_info('select DEAT from indi where INDI == "{}"'.format(parent[0][1]))
                    if alive1[0][0] != 'NA' and alive2[0][0] != 'NA':
                        status = False
                        print("US33: Orphan {} {} found in family {}.".format(person[0], person[4], person[3]))

        return status

    def list_large_age_differences(self):
        """
        Author: Mutni
        US34 List all couples who were married when the older spouse was more than twice as old as the younger spouse
        :return:
        """
        status = True
        query = 'select fam.HUSB, fam.WIFE, fam.MARR from fam'  # get couples
        couples = self.tool.query_info(query)
        for couple in couples:
            husband_birth = self.tool.query_info('select BIRT, NAME from indi where indi == "{}"'.format(couple[0]))
            husband_marry_age = self.tool.get_age(husband_birth[0][0], couple[2])
            wife_birth = self.tool.query_info('select BIRT, NAME from indi where indi == "{}"'.format(couple[1]))
            wife_marry_age = self.tool.get_age(wife_birth[0][0], couple[2])
            if husband_marry_age > 0 and wife_marry_age > 0:  # validate
                if husband_marry_age / wife_marry_age > 2 or wife_marry_age / husband_marry_age > 2:
                    status = False
                    print("US34: {} and {} married when the older spouse was more than twice as old as the younger."
                          .format(husband_birth[0][1], wife_birth[0][1]))
        return status

    def list_recent_births(self):
        """
        Author Robyn
        US35
        :return:

        """
        status = True
        individuals = self.tool.query_info('select INDI, NAME, BIRT from indi')
        thirty_days = relativedelta(days=30)
        for indi in list(individuals):
            print(indi)
            birth = indi[2]
            if self.tool.dates_within(person[2], str(self.tool.today - thirty_days), 30, 'days'):
                status = False
                print("US35: {} {} was born within the last 30 days on {}."
                      .format(indi[0], indi[1], indi[2]))
        pass

    def list_recent_deaths(self):
        """
        Author Robyn
        US36
        :return:
        """
        status = True
        individuals = self.tool.query_info('select INDI, NAME, DEAT from indi')
        thirty_days = relativedelta(days=30)
        for indi in list(individuals):
            print(indi)
            birth = indi[2]
            if self.tool.dates_within(person[2], str(self.tool.today - thirty_days), 30, 'days'):
                status = False
                print("US35: {} {} was died within the last 30 days on {}."
                      .format(indi[0], indi[1], indi[2]))
        pass

    def list_upcoming_birthdays(self):
        """
        US38 List all living people in a GEDCOM file whose birthdays occur in the next 30 days
        :return:bool
        """
        status = True
        query = 'select INDI, NAME, BIRT from indi where DEAT == "NA"'  # get living people
        thirty_days = relativedelta(days=30)
        people = self.tool.query_info(query)
        for person in people:
            if self.tool.dates_within(str(self.tool.today.year) + person[2][-6:],
                                      str(self.tool.today + thirty_days), 30, 'days'):
                status = False
                print("US38: {} {}'s birthday will occur in the next 30 days on {}."
                      .format(person[0], person[1], person[2]))
        return status

    def list_upcoming_anniversaries(self):
        """
        US39 List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days
        :return:bool
        """
        status = True
        thirty_days = relativedelta(days=30)
        query = 'select fam.HUSB, fam.WIFE, fam.MARR from fam'  # get couples
        couples = self.tool.query_info(query)
        for couple in couples:
            dead1 = self.tool.query_info('select NAME from indi where DEAT == "NA" and INDI == "{}"'.format(couple[0]))
            dead2 = self.tool.query_info('select NAME from indi where DEAT == "NA" and INDI == "{}"'.format(couple[1]))
            if len(dead1) != 0 and len(dead2) != 0:
                if self.tool.dates_within(str(self.tool.today.year) + couple[2][-6:],
                                          str(self.tool.today + thirty_days), 30, 'days'):
                    status = False
                    print("US39: {} and {} will have their marriage anniversary in the next 30 days on {}."
                          .format(dead1[0][0], dead2[0][0], couple[2][-5:]))
        return status


class TestSprint4(unittest.TestCase):  # TODO: uncomment your test case to test your US
    """
    Unittest for Sprint 4.
    """

    def setUp(self):
        self.test = Sprint4()

    def test_list_living_single(self):
        self.assertFalse(self.test.list_living_single())
    
    def test_list_multiple_births(self):
        self.assertFalse(self.test.list_multiple_births())

    def test_list_orphans(self):
        self.assertFalse(self.test.list_orphans())

    def test_list_large_age_differences(self):
        self.assertFalse(self.test.list_large_age_differences())

    def test_list_recent_births(self):
        self.assertFalse(self.test.list_recent_births())
    
    def test_list_recent_deaths(self):
        self.assertFalse(self.test.list_recent_deaths())

    def test_list_upcoming_birthdays(self):
        self.assertFalse(self.test.list_upcoming_birthdays())

    def test_list_upcoming_anniversaries(self):
        self.assertFalse(self.test.list_upcoming_anniversaries())


class RunSprints:
    """
    Wrapper class for all Sprints.
    """
    def __init__(self):
        self.util = ProjectUtil()
        self.sprint1 = Sprint1()
        self.sprint2 = Sprint2()
        self.sprint3 = Sprint3()

    def run(self):
        self.util.print_info()
        self.sprint1.run_sprint1()
        self.util.disconnect()


def main():
    demo = RunSprints()
    demo.run()


if __name__ == '__main__':
    main()
    unittest.main()

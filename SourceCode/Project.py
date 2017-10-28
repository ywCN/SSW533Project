import sqlite3
import os
import unittest
from datetime import datetime
from prettytable import PrettyTable


class ProjectUtil:
    """
    This class contains all utility methods.
    """
    def __init__(self):
        self.db = r'project.db'
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

    def convert_to_datetime(self, date):
        """
        :param date: str
        :return: datatime type or str "NA"
        """
        try:
            res = datetime.strptime(date, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            res = "NA"
        return res

    def combine_id_name(self, indi, name):
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
        for person in deads:
            death = person[2]
            if person[1] == 'M':
                query2 = 'select fam.CHIL from fam where fam.HUSB == "{}"'.format(person[0])  # list of children
                children = self.tool.query_info(query2)
                for child in children[0]:
                    query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'.format(child)  # birthday
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
                    query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'.format(child)  # birthday
                    birth = self.tool.query_info(query3)
                    if not self.tool.date_before(death, birth):
                        status = False
                        print("ERROR: US09: {} is born after death of mother {}.".format(birth[1], person[3]))
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


# class TestSprint2(unittest.TestCase):  #TODO: uncomment this after finishing Sprint3
#     """
#     Unittest for Sprint 2.
#     """
#
#     def setUp(self):
#         self.test = Sprint2()
#
#     def test_birth_before_death_of_parents(self):
#         self.assertFalse(self.test.birth_before_death_of_parents())
#
#     def test_parent_not_too_old(self):
#         self.assertFalse(self.test.parent_not_too_old())
#
#     def test_siblings_spacing(self):
#         self.assertFalse(self.test.siblings_spacing())
#
#     def test_multiple_births_less_than_5(self):
#         self.assertFalse(self.test.multiple_births_less_than_5())
#
#     def test_fewer_than_15_siblings(self):
#         self.assertFalse(self.test.fewer_than_15_siblings())
#
#     def test_male_last_names(self):
#         self.assertFalse(self.test.male_last_names())
#
#     def test_marriage_after_14(self):
#         self.assertFalse(self.test.marriage_after_14())
#
#     def test_siblings_should_not_marry(self):
#         self.assertFalse(self.test.siblings_should_not_marry())


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
        NB = self.tool.query_info(query)
        dup_name = NB[0][0]
        dup_birt = NB[0][1]
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
        HW = self.tool.query_info(query)
        for correct in HW:
            husband = self.tool.query_info('select INDI, NAME, SEX from indi where INDI == "{}"'.format(correct[0]))[0]
            wife = self.tool.query_info('select INDI, NAME, SEX from indi where INDI == "{}"'.format(correct[1]))[0]
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
        # TODO: fill in your logic here to detect wrong data. Set status False when detecting one.
        return status

    def order_siblings_by_age(self):
        """
        US28
        author: Robyn
        :return: bool
        """
        status = True
        # TODO: fill in your logic here to detect wrong data. Set status False when detecting one.
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

    def run_sprint3(self):  # TODO: delete this method after finishing Sprint 3 as test case will run all the methods
        # self.tool.print_info()
        # self.unique_name_and_birth_date()
        # self.correct_gender_for_role()
        # self.unique_ids()
        # self.unique_first_names_in_families()
        self.include_individual_ages()
        self.order_siblings_by_age()
        # self.list_deceased()
        # self.list_living_married()
        # self.tool.disconnect()


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
#
#     def test_include_individual_ages(self):
#         self.assertFalse(self.test.include_individual_ages())
#
#     def test_order_siblings_by_age(self):
#         self.assertFalse(self.test.order_siblings_by_age())

    def test_list_deceased(self):
        self.assertFalse(self.test.list_deceased())

    def test_list_living_married(self):
        self.assertFalse(self.test.list_living_married())


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
        # self.sprint1.run_sprint1() # TODO: uncomment this after finishing Sprint3
        # self.sprint2.run_sprint2()  # no need to run because unittest will run all methods
        self.sprint3.run_sprint3()
        self.util.disconnect()


def main():
    demo = RunSprints()
    demo.run()


if __name__ == '__main__':
    main()
    unittest.main()

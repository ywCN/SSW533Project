import sqlite3
import os
import unittest
from datetime import datetime
from prettytable import PrettyTable


'''
Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''


class Project6:
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

    def dates_before_current_date(self):
        """
        US01 - Dates before current date
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT, fam.MARR, fam.DIV from indi LEFT JOIN fam ON INDI.INDI = FAM.HUSB OR " \
                "INDI.INDI = FAM.WIFE "

        for row in self.query_info(query):
            dates = [row[2], row[3], row[4], row[5]]
            for date in dates:
                if not self.before_today(date):
                    print("ERROR: US01: {} occurs after today {} for {}"
                          .format(date, self.today, self.combine_id_name(row[0], row[1])))

    def birth_before_marriage(self):
        """
        US02 - Birth before marriage
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, fam.MARR from indi INNER JOIN fam ON INDI.INDI = FAM.HUSB OR INDI.INDI = " \
                "FAM.WIFE "
        for row in self.query_info(query):
            birth = row[2]
            marriage = row[3]
            if not self.date_before(birth, marriage):
                print("ERROR: US02: Birth {} occurs after marriage {} for {}"
                      .format(birth, marriage, self.combine_id_name(row[0], row[1])))

    def birth_before_death(self):
        """
        US03 - Birth before death
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.query_info(query):
            birth = row[2]
            death = row[3]
            if not self.date_before(birth, death):
                print("ERROR: US03: Birth {} occurs after death {} for {}"
                      .format(birth, death, self.combine_id_name(row[0], row[1])))

    def marriage_before_divorce(self):
        """
        US04 - Marriage before divorce
        :rtype: None
        """
        query = "select INDI, NAME, fam.MARR, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        for row in self.query_info(query):
            marry = row[2]
            divorce = row[3]
            if not self.date_before(marry, divorce):
                print("ERROR: US04: Marriage {} occurs after divorce {} for {}"
                      .format(marry, divorce, self.combine_id_name(row[0], row[1])))

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
            if not self.date_before(marry, death):
                print("ERROR: US05: Marriage {} occurs after death {} for {}"
                      .format(marry, death, self.combine_id_name(row[0], row[1])))

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
            if not self.date_before(divorce, death):
                print("ERROR: US06: Divorce {} occurs after death {} for {}"
                      .format(divorce, death, self.combine_id_name(row[0], row[1])))

    def less_than_150_years_old(self):
        """
        US07 - Less then 150 years old
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.query_info(query):
            if self.get_age(row[2], row[3]) >= 150:
                print("ERROR: US07: Age is greater than or equal to 150 years for {}"
                      .format(self.combine_id_name(row[0], row[1])))

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
            if not self.date_before(marry, birth):
                print("ERROR: US08: Parent marriage {} after birth {} of {}"
                      .format(marry, birth, self.combine_id_name(row[0], row[1])))
            if self.date_before(divorce, birth) and not self.dates_within(divorce, birth, 9, "months"):
                print("ERROR: US08: {} was born {} after 9 months of parent divorce {}".format(
                    self.combine_id_name(row[0], row[1]), birth, divorce))

    def birth_before_death_of_parents(self):
        """
        US09
        Child should be born before death of mother and before 9 months after death of father
        :return: bool
        """
        status = True
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
                    birth = data[0][1]
                    name = data[0][1]
                    if self.date_before(death, birth) and self.dates_within(death, birth, 9, 'months'):
                        status = False
                        print("ERROR: US09: {} is born 9 months after death of father {}.".format(birth, name))
            if person[1] == 'F':
                query2 = 'select fam.CHIL from fam where fam.WIFE == "{}"'.format(person[0])
                children = self.query_info(query2)
                for child in children[0]:
                    query3 = 'select indi.BIRT, indi.NAME from indi where indi.INDI == "{}"'.format(child)  # birthday
                    birth = self.query_info(query3)
                    if not self.date_before(death, birth):
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
        children = self.query_info(query1)
        for child in children:
            birth = child[1]
            query2 = 'select fam.HUSB, fam.WIFE from fam where fam.FAM == "{}"'.format(child[2])
            parents = self.query_info(query2)  # parent ids (male, female)
            father_birth = self.query_info('select indi.BIRT from indi where indi.INDI == "{}"'.format(parents[0][0]))[0][0]
            mother_birth = self.query_info('select indi.BIRT from indi where indi.INDI == "{}"'.format(parents[0][1]))[0][0]
            if self.date_before(mother_birth, birth) and not self.dates_within(mother_birth, birth, 60, 'years'):
                status = False
                print("ERROR: US12: Mother is not less than 60 years older than her children {}.".format(child[3]))
            if self.date_before(father_birth, birth) and not self.dates_within(father_birth, birth, 80, 'years'):
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
        siblings = self.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 1:
                for a in sib:
                    for b in sib:
                        birth_a = self.get_birthday(a)
                        birth_b = self.get_birthday(b)
                        if not self.dates_within(birth_a, birth_b, 2, 'days') and self.dates_within(birth_a, birth_b, 8, 'months'):
                            status = False
                            print("ERROR: US13: Birthday of {} and {} is less than 8 months apart or more than 2 days apart.".format(self.get_name(a), self.get_name(b)))
        return status

    def multiple_births_less_than_5(self):
        """
        US14
        No more than five siblings should be born at the same time
        :return: bool
        """
        status = True
        query = 'select fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'
        siblings = self.query_info(query)
        for sibling in siblings:
            sib = sibling[0].split()
            if len(sib) > 5:
                counter = 0
                for i in range(len(sib) - 1):
                    prev = self.get_birthday(sib[i])
                    next = self.get_birthday(sib[i + 1])
                    if self.dates_within(prev, next, 1, 'days'):
                        counter += 1
                        if counter > 5:
                            status = False
                            print("ERROR: US14: There are more than five siblings born at the same time in family {}.".format(sibling[1]))
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
        siblings = self.query_info(query)
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
        query1 = 'select fam.HUSB, fam.CHIL, fam.FAM from fam where fam.CHIL != "NA"'  # all males in a family
        males_fam = self.query_info(query1)
        for males in males_fam:
            # print(type(males[1]))  # string
            ids = (males[0] + " " + males[1]).split()
            # print(self.get_name(ids[0]).split('/')[1])  # last name
            flag = False
            for a in ids:
                for b in ids:
                    name_a = self.get_name(a).split('/')[1]
                    name_b = self.get_name(b).split('/')[1]
                    if name_a != name_b:
                        flag = True
                        status = False
                        break
            if flag:
                print("ERROR: US16: Not all male members of family {} have the same last name.".format(males[2]))
        # TODO: make name lists, for each id in list, check if male

        return status

    def marriage_after_14(self):
        """
        US10
        Marriage should be at least 14 years after birth of both spouses
        (parents must be at least 14 years old)
        :return: bool
        """
        status = True

        return status

    def siblings_should_not_marry(self):
        """
        US18
        Siblings should not marry one another
        :return: bool
        """
        status = True

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
        # self.birth_before_death_of_parents()  # test case will run the method
        # self.parent_not_too_old()
        # self.siblings_spacing()
        # self.multiple_births_less_than_5()
        # self.fewer_than_15_siblings()
        self.male_last_names()
        self.marriage_after_14()
        self.siblings_should_not_marry()
        self.disconnect()


class TestSprint2(unittest.TestCase):
    def test_birth_before_death_of_parents(self):
        test = Project6()
        self.assertFalse(test.birth_before_death_of_parents())

    def test_parent_not_too_old(self):
        test = Project6()
        self.assertFalse(test.parent_not_too_old())

    def test_siblings_spacing(self):
        test = Project6()
        self.assertFalse(test.siblings_spacing())

    def test_multiple_births_less_than_5(self):
        test = Project6()
        self.assertFalse(test.multiple_births_less_than_5())

    def test_fewer_than_15_siblings(self):
        test = Project6()
        self.assertFalse(test.fewer_than_15_siblings())

#     def test_male_last_names(self):
#         test = Project6()
#         self.assertFalse(test.male_last_names())
#
#     def test_marriage_after_14(self):
#         test = Project6()
#         self.assertFalse(test.marriage_after_14())
#
#     def test_siblings_should_not_marry(self):
#         test = Project6()
#         self.assertFalse(test.siblings_should_not_marry())


def main():
    demo = Project6()
    # demo.run_sprint1()
    demo.run_sprint2()


if __name__ == '__main__':
    main()
    unittest.main()

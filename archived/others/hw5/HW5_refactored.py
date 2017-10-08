import sqlite3
import os
from datetime import datetime
from prettytable import PrettyTable


'''
Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''


class HW5:
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
            # birth = self.convert_to_datetime(row[2])
            # death = self.convert_to_datetime(row[3])
            # marriage = self.convert_to_datetime(row[4])
            # divorce = self.convert_to_datetime(row[5])
            # dates = [birth, death, marriage, divorce]
            dates = [row[2], row[3], row[4], row[5]]
            for date in dates:
                # if date != "NA" and date > self.today:
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
            birth = self.convert_to_datetime(row[2])
            death = self.convert_to_datetime(row[3])
            if death != "NA" and birth > death:
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
            if row[3] != "NA":
                marry = self.convert_to_datetime(row[2])
                divorce = self.convert_to_datetime(row[3])
                if marry > divorce:
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
            if row[2] != "NA":
                death = self.convert_to_datetime(row[2])
                marry = self.convert_to_datetime(row[3])
                if marry > death:  # cannot marry after death
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
            if row[2] != "NA" and row[3] != "NA":
                death = self.convert_to_datetime(row[2])
                divorce = self.convert_to_datetime(row[3])
                if divorce > death:  # cannot divorce after death
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
            birth = self.convert_to_datetime(row[2])
            marry = self.convert_to_datetime(row[3])
            divorce = self.convert_to_datetime(row[4])
            if marry != "NA" and birth < marry:
                print("ERROR: US08: Parent marriage {} after birth {} of {}"
                      .format(marry, birth, self.combine_id_name(row[0], row[1])))
            if divorce != "NA" and divorce > birth and not self.dates_within(divorce, birth, 9, "months"):
                print("ERROR: US08: {} was born {} after 9 months of divorce {}".format(
                    self.combine_id_name(row[0], row[1]), birth, divorce))

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
        if unit not in self.conversion:
            raise Exception("No such unit")
        return (abs((dt1 - dt2).days) / self.conversion[unit]) <= limit

    def date_before(self, before, after):
        """
        check if before date happens after after date
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
        self.print_info()
        self.dates_before_current_date()
        self.birth_before_marriage()
        self.birth_before_death()
        self.marriage_before_divorce()
        self.marriage_before_death()
        self.divorce_before_death()
        self.less_than_150_years_old()
        self.birth_before_marriage_of_parents()
        self.disconnect()


def main():
    demo = HW5()
    demo.run_sprint1()


if __name__ == '__main__':
    main()

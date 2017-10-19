import sqlite3
import os
from datetime import datetime
from prettytable import PrettyTable

"""
This class contains all utility methods.
"""


class ProjectUtil:

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
import sqlite3
import os
from datetime import datetime
from prettytable import PrettyTable


'''
Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''


class HW4:
    def __init__(self):
        self.db = r'project.db'
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
        :rtype: bool
        """
        query = "select INDI, NAME, BIRT, DEAT, fam.MARR, fam.DIV from indi LEFT JOIN fam ON INDI.INDI = FAM.HUSB OR " \
                "INDI.INDI = FAM.WIFE "
        today = datetime.today().date()

        for row in self.query_info(query):
            birth = datetime.strptime(row[2], '%Y-%m-%d').date()
            death = datetime.strptime(row[3], '%Y-%m-%d').date()
            if not row[4]:
                marriage = datetime.strptime(row[4], '%Y-%m-%d').date()
            else:
                marriage = "NA"
            divorce = datetime.strptime(row[5], '%Y-%m-%d').date()
            dates = [birth, death, marriage, divorce]
            for date in dates:
                if date != "NA" and date > today:
                    print("ERROR: US01: {} occurs after today {} for {}".format(date, today, row[0] + row[1]))

    def birth_before_marriage(self):
        """
        US02 - Birth before marriage
        :rtype: bool
        """
        query = "select INDI, NAME, BIRT, fam.MARR from indi INNER JOIN fam ON INDI.INDI = FAM.HUSB OR INDI.INDI = " \
                "FAM.WIFE "
        for row in self.query_info(query):
            if row[3] != "NA":
                birth = datetime.strptime(row[2], '%Y-%m-%d').date()
                marriage = datetime.strptime(row[3], '%Y-%m-%d').date()
                if birth > marriage:
                    print("ERROR: US02: Birth {} occurs after marriage {} for {}".format(birth, marriage, row[0] + row[1]))

    def birth_before_death(self):
        """
        US03 - Birth before death
        :rtype: bool
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.query_info(query):
            if row[3] != "NA":
                birth = datetime.strptime(row[2], '%Y-%m-%d').date()
                death = datetime.strptime(row[3], '%Y-%m-%d').date()
                if birth > death:
                    print("ERROR: US03: Birth {} occurs after death {} for {}".format(birth, death, row[0] + row[1]))

    def marriage_before_divorce(self):
        """
        US04 - Marriage before divorce
        :rtype: bool
        """
        query = "select INDI, NAME, fam.MARR, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        for row in self.query_info(query):
            if row[3] != "NA":
                marry = datetime.strptime(row[2], '%Y-%m-%d').date()
                divorce = datetime.strptime(row[3], '%Y-%m-%d').date()
                if marry > divorce:
                    print("ERROR: US04: Marriage {} occurs after divorce {} for {}".format(marry, divorce, row[0] + row[1]))

    def marriage_before_death(self):
        """
        US05 - Marriage before death
        :rtype: bool
        """
        query = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            if row[2] != "NA":
                death = datetime.strptime(row[2], '%Y-%m-%d').date()
                marry = datetime.strptime(row[3], '%Y-%m-%d').date()
                if marry > death:  # cannot marry after death
                    print("ERROR: US05: Marriage {} occurs after death {} for {}".format(marry, death, row[0] + row[1]))
                    return False
        return True

    def divorce_before_death(self):
        """
        US06 - Divorce before death
        :rtype: bool
        """
        query = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            if row[2] != "NA" and row[3] != "NA":
                death = datetime.strptime(row[2], '%Y-%m-%d').date()
                divorce = datetime.strptime(row[3], '%Y-%m-%d').date()
                if divorce > death:  # cannot divorce after death
                    print("ERROR: US06: Divorce {} occurs after death {} for {}".format(divorce, death, row[0] + row[1]))
                    return False
        return True

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

    def print_everything(self):
        query1 =""
        query2 =""

    def run_sprint1(self):
        self.dates_before_current_date()
        self.birth_before_marriage()
        self.birth_before_death()
        self.marriage_before_divorce()
        self.marriage_before_death()
        self.divorce_before_death()



def main():
    demo = HW4()
    demo.run_sprint1()
    demo.disconnect()


if __name__ == '__main__':
    main()

import sqlite3
import unittest
from datetime import datetime

'''
Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''

class HW4:

    def __init__(self):
        self.conn = sqlite3.connect('project.db')
        self.c = self.conn.cursor()

    def marriage_before_death(self):
        """
        :rtype: bool
        """
        query = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            if row[2] != "NA":
                death = datetime.strptime(row[2], '%Y-%m-%d').date()
                marry = datetime.strptime(row[3], '%Y-%m-%d').date()
                if marry > death:  # cannot marry after death
                    return False
        return True

    def divorce_before_death(self):
        """
        :rtype: bool
        """
        query = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.query_info(query):
            if row[2] != "NA" and row[3] != "NA":
                death = datetime.strptime(row[2], '%Y-%m-%d').date()
                divorce = datetime.strptime(row[3], '%Y-%m-%d').date()
                if divorce > death:  # cannot divorce after death
                    return False

        return True

    def query_info(self, query):
        """
        :type query: str
        :rtype: List[List[str]]
        """
        self.c.execute("%s" % query)
        return self.c.fetchall()


class TestHW4:

    def test_marriage_before_death(self):
        expected = True

    def divorce_before_death(self):
        expected = True

    def query_info(self):
        test_query1 = ""
        test_query2 = ""
        test_query3 = ""

def main():
    demo = HW4()
    print(demo.marriage_before_death())
    print(demo.divorce_before_death())

if __name__ == '__main__':
    main()

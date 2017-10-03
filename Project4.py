import sqlite3
import unittest
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

    def marriage_before_death(self):
        """
        US05 - Marriage before death
        :rtype: null
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


class TestHW4(unittest.TestCase):
    def test_marriage_before_death(self):
        expected = True  # because my data is valid, invalid data won't pass test
        unexpected = False  # This should not happen if the given data is valid.
        self.assertTrue(HW4().marriage_before_death())
        self.assertTrue(HW4().marriage_before_death() == expected)
        self.assertFalse(HW4().marriage_before_death() == unexpected)

    def test_divorce_before_death(self):
        expected = True
        unexpected = False
        self.assertTrue(HW4().divorce_before_death())
        self.assertTrue(HW4().divorce_before_death() == expected)
        self.assertFalse(HW4().divorce_before_death() == unexpected)

    def test_query_info(self):
        test_query1 = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                      "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        test_query2 = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                      "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        self.assertEqual(len(HW4().query_info(test_query1)[0]), 4)
        self.assertEqual(len(HW4().query_info(test_query1)), 8)
        self.assertEqual(len(HW4().query_info(test_query2)[0]), 4)
        self.assertEqual(len(HW4().query_info(test_query2)), 8)


def main():
    demo = HW4()
    if demo.marriage_before_death():
        print("All marriages are before death.")
    else:
        print("Not all marriages are before death.\nPlease check your file.")
    if demo.divorce_before_death():
        print("All divorces are before death.")
    else:
        print("Not all divorces are before death.\nPlease check your file.")
    demo.disconnect()


if __name__ == '__main__':
    main()
    unittest.main()

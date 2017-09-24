import sqlite3
import unittest

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
        query = ""

        print("invalid INDI")
        return False

        return True

    def divorce_before_death(self):
        """
        :rtype: bool
        """
        query = ""

        print("invalid INDI")
        return False

        return True

    def query_info(self, query):
        """
        :type query: str
        :rtype: bool
        """


class TestHW4:

    def test_marriage_before_death(self):
        expected = True

    def divorce_before_death(self):
        expected = True

    def query_info(self):
        test_query1 = ""
        test_query2 = ""
        test_query3 = ""
import unittest
import ProjectClass as db
import USLogic as us

'''
This py file contains the Test Classes
Use these Classes to test the functionality of USLogic and GenFxns
'''

class TestUS(unittest.TestCase):
    def setUp(self):
        #self.testDemo = db.Project()
        return

    def testUS03_NA(self):
        row = ["I5", "Ping /Ju/", "1950-06-23", "NA"]
        self.assertTrue(us.checkRow_US03(row))
        return

    def testUS03_Correct(self):
        row = ["I7", "Fu /Tian/", "1965-07-15" ,"3008-11-18"]
        self.assertTrue(us.checkRow_US03(row))
        return

    def testUS03_Incorrect(self):
        row = ["I2", "San /Wang/", "1967-06-04", "1008-11-18"]
        self.assertFalse(us.checkRow_US03(row))
        return

    def tearDown(self):
        #self.testDemo.disconnect()
        return

class Test_Sprint2(unittest.TestCase):
    def testUS09_InCorrect(self):
        test = db.Project()
        self.assertFalse(us.checkDates_US09("1000-11-18", "1995-04-07", True))
        self.assertFalse(us.checkDates_US09("1000-01-01", "1000-03-01", True))
        test.disconnect
        return

    def testUS09_Correct(self):
        test = db.Project()
        self.assertTrue(us.checkDates_US09("3008-11-18", "1995-04-07", True))
        test.disconnect
        return

    def testUS12_InCorrect(self):
        self.assertFalse(us.checkFatherCase_US12("1190-01-01", "1000-01-01"))
        self.assertFalse(us.checkMotherCase_US12("1190-01-01", "1000-01-01"))
        return

    def testUS12_Correct(self):
        self.assertTrue(us.checkFatherCase_US12("1025-01-01", "1000-01-01"))
        self.assertTrue(us.checkMotherCase_US12("1025-01-01", "1000-01-01"))
        return

    def testUS13_InCorrect(self):
        self.assertFalse(us.checkSiblingBirthdays_US13("1000-05-01", "1000-01-01"))
        return

    def testUS13_Correct(self):
        self.assertTrue(us.checkSiblingBirthdays_US13("1001-05-01", "1000-01-01"))
        return

    def testUS14_InCorrect(self):
        test = db.Project()
        self.assertFalse(us.checkMultBirths_US14(test, ['I11', 'I12', 'I13', 'I14', 'I15', 'I16', 'I17', 'I18', 'I19', 'I20', 'I21', 'I22', 'I23', 'I24', 'I25', 'I26', 'I27']))
        test.disconnect
        return

    def testUS15_Correct(self):
        self.assertTrue(us.checkSiblings_US15('I1'))
        self.assertTrue(us.checkSiblings_US15('I1, I2'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12, I13'))
        self.assertTrue(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12, I13, I14'))
        return
    
    def testUS15_Incorrect(self):
        self.assertFalse(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12, I13, I14, I15'))
        self.assertFalse(us.checkSiblings_US15('I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12, I13, I14, I15, I16'))
        return

    def testUS16_Correct(self):
        testing = db.Project()
        familyInfo = ["I4", "I2 I6", "F2"]
        self.assertTrue(us.checkMaleLastNames_US16(testing,familyInfo))
        familyInfo = ["I8", "I10", "F3"]
        self.assertTrue(us.checkMaleLastNames_US16(testing, familyInfo))
        familyInfo = ["I7", "I9", "F4"]
        self.assertTrue(us.checkMaleLastNames_US16(testing, familyInfo))
        testing.disconnect()
        return

    def testUS16_Incorrect(self):
        test = db.Project()
        familyInfo = ["I1", "I11 I12 I13 I14 I15 I16 I17 I18 I19 I20 I21 I22 I23 I24 I25 I26 I27", "F5"]
        self.assertFalse(us.checkMaleLastNames_US16(test, familyInfo))
        test.disconnect
        return

    def testUS10_InCorrect(self):
        self.assertFalse(us.checkMarriage_US10("1948-07-11", "1950-06-23", "1952-08-13"))
        return

    def testUS10_Correct(self):
        self.assertTrue(us.checkMarriage_US10("2666-08-06", "1666-06-06", "1703-07-08"))
        return

    def testUS18_MarriedSibs(self):
        self.assertTrue(us.checkMarriedSiblings_US18('I24', 'I25' , 'I11 I12 I13 I14 I15 I16 I17 I18 I19 I20 I21 I22 I23 I24 I25 I26 I27'))
        return

    def testUS18_NotSibs(self):
        self.assertFalse(us.checkMarriedSiblings_US18('I24', 'I4' , 'I11 I12 I13 I14 I15 I16 I17 I18 I19 I20 I21 I22 I23 I24 I25 I26 I27'))
        return

class TestGenFxn(unittest.TestCase):
    def setUp(self):
        #self.testDemo = db.Project()
        return

    #TODO

    def tearDown(self):
        #self.testDemo.disconnect()
        return


'''
#This class is not for general unit testing, but as a basic check on the functionality of the current Sprint
class OUTDATED(unittest.TestCase):
    def setUp(self):
        self.test = db.Project()

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
    
    def tearDown(self):
        self.test.disconnect()
        return
'''

if __name__ == "__main__":
    #test = db.Project()
    #familyInfo = ["I4", "I2 I6", "F2"]
    #print(us.checkMaleLastNames_US16(test, familyInfo))
    unittest.main()

    

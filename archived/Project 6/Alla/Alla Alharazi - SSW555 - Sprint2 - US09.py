#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 06:19:46 2017

@author: allo0o2a
"""
from datetime import date
from dateutil.relativedelta import relativedelta
import sys
import unittest

# US09: Birth before death of parents 
# Child should be born:
# before death of mother 
# before 9 months after death of father

def check_birth_before_death_of_parents(DOBChild, DODFather, DODMother):
    Addninemonths = relativedelta(months=9)
    C = DODFather + Addninemonths
    if DOBChild < C and DOBChild < DODMother:
        return ("The child born before 9 months after death of father.") 
    else:
        return ("The child can not born after 9 months after death of father or after mother death.")
        
         
class TestSprint2(unittest.TestCase):
    
    def test_check_birth_before_death_of_parents(self):
        DOBC = date(2017,11,14)
        
        DODF1 = date(2017,2,14) #no
        DODM1 = date(2017,10,12)#no
        
        DODF2 = date(2017,6,14)#yes
        DODM2 = date(2017,11,15)#yes

        self.assertEqual(check_birth_before_death_of_parents(DOBC,DODF1,DODM1),"The child can not born after 9 months after death of father or after mother death.")
        self.assertEqual(check_birth_before_death_of_parents(DOBC,DODF2,DODM2),"The child born before 9 months after death of father.")
        self.assertEqual(check_birth_before_death_of_parents(DOBC,DODF1,DODM2),"The child can not born after 9 months after death of father or after mother death.")
        self.assertEqual(check_birth_before_death_of_parents(DOBC,DODF2,DODM1),"The child can not born after 9 months after death of father or after mother death.")

def main():
    try:
        print("You can just use: YYYY-MM-DD format")
        
        DOM0 = input('Please enter the DOB of the Child: ')
        year0, month0, day0 = map(int, DOM0.split('-'))
        
        DOM1 = input('Please enter the DOD of the Father: ')
        year1, month1, day1 = map(int, DOM1.split('-'))
        
        DOM2 = input('Please enter the DOD of the Mother: ')
        year2, month2, day2 = map(int, DOM2.split('-'))
        
        check_birth_before_death_of_parents(date(year0, month0, day0),date(year1, month1, day1),date(year2, month2, day2))
        
    except:
        print ("Please enter a valid date.")
        sys.exit()

 
if __name__ == '__main__':
    #main()
    unittest.main(exit=False, verbosity=2) 

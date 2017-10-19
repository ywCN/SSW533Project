import unittest
from SourceCode.ProjectUtil import ProjectUtil


'''
Our team is using database solution.
Please put the .db file in the same path of this .py file.
'''


class Sprint2:
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
            if self.tool.date_before(mother_birth, birth) and not self.tool.dates_within(mother_birth, birth, 60, 'years'):
                status = False
                print("ERROR: US12: Mother is not less than 60 years older than her children {}.".format(child[3]))
            if self.tool.date_before(father_birth, birth) and not self.tool.dates_within(father_birth, birth, 80, 'years'):
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
            # print(type(males[1]))  # string
            ids = (males[0] + " " + males[1]).split()
            # print(self.get_name(ids[0]).split('/')[1])  # last name
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
            # print(len(couple))  # 3
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
        # print(len(sibling_lists))  # 5
        query2 = 'select fam.HUSB, fam.WIFE from fam'  # get couples
        couples = self.tool.query_info(query2)
        # print(len(couples))  # 6
        for couple in couples:
            p1 = couple[0]
            p2 = couple[1]
            for sibling_list in sibling_lists:
                if p1 in sibling_list[0] and p2 in sibling_list[0]:
                    status = False
                    print("ERROR: US18: Siblings {} and {} married.".format(p1, p2))

        return status

    # def run_sprint2(self):
    #     self.print_info()
    #     # self.birth_before_death_of_parents()  # test case will run the method
    #     # self.parent_not_too_old()
    #     # self.siblings_spacing()
    #     # self.multiple_births_less_than_5()
    #     # self.fewer_than_15_siblings()
    #     # self.male_last_names()
    #     # self.marriage_after_14()
    #     # self.siblings_should_not_marry()
    #     self.disconnect()


class TestSprint2(unittest.TestCase):
    ProjectUtil().print_info()

    def setUp(self):
        self.test = Sprint2()

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

    ProjectUtil().disconnect()


# def main():
#     demo = Project6()
#     demo.run_sprint1()
#     demo.run_sprint2()  # no need to run because unittest will run all methods.


if __name__ == '__main__':
    # main()
    unittest.main()

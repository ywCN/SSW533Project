from SourceCode.ProjectUtil import ProjectUtil


class Sprint1:
    def __init__(self):
        self.tool = ProjectUtil()  # get tools ready

    def dates_before_current_date(self):
        """
        US01 - Dates before current date
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT, fam.MARR, fam.DIV from indi LEFT JOIN fam ON INDI.INDI = FAM.HUSB OR " \
                "INDI.INDI = FAM.WIFE "

        for row in self.tool.query_info(query):
            dates = [row[2], row[3], row[4], row[5]]
            for date in dates:
                if not self.tool.before_today(date):
                    print("ERROR: US01: {} occurs after today {} for {}"
                          .format(date, self.tool.today, self.tool.combine_id_name(row[0], row[1])))

    def birth_before_marriage(self):
        """
        US02 - Birth before marriage
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, fam.MARR from indi INNER JOIN fam ON INDI.INDI = FAM.HUSB OR INDI.INDI = " \
                "FAM.WIFE "
        for row in self.tool.query_info(query):
            birth = row[2]
            marriage = row[3]
            if not self.tool.date_before(birth, marriage):
                print("ERROR: US02: Birth {} occurs after marriage {} for {}"
                      .format(birth, marriage, self.tool.combine_id_name(row[0], row[1])))

    def birth_before_death(self):
        """
        US03 - Birth before death
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.tool.query_info(query):
            birth = row[2]
            death = row[3]
            if not self.tool.date_before(birth, death):
                print("ERROR: US03: Birth {} occurs after death {} for {}"
                      .format(birth, death, self.tool.combine_id_name(row[0], row[1])))

    def marriage_before_divorce(self):
        """
        US04 - Marriage before divorce
        :rtype: None
        """
        query = "select INDI, NAME, fam.MARR, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"
        for row in self.tool.query_info(query):
            marry = row[2]
            divorce = row[3]
            if not self.tool.date_before(marry, divorce):
                print("ERROR: US04: Marriage {} occurs after divorce {} for {}"
                      .format(marry, divorce, self.tool.combine_id_name(row[0], row[1])))

    def marriage_before_death(self):
        """
        US05 - Marriage before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.MARR from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.tool.query_info(query):
            death = row[2]
            marry = row[3]
            if not self.tool.date_before(marry, death):
                print("ERROR: US05: Marriage {} occurs after death {} for {}"
                      .format(marry, death, self.tool.combine_id_name(row[0], row[1])))

    def divorce_before_death(self):
        """
        US06 - Divorce before death
        :rtype: None
        """
        query = "select INDI, NAME, DEAT, fam.DIV from indi INNER JOIN fam " \
                "ON INDI.INDI = FAM.HUSB OR INDI.INDI = FAM.WIFE"

        for row in self.tool.query_info(query):
            death = row[2]
            divorce = row[3]
            if not self.tool.date_before(divorce, death):
                print("ERROR: US06: Divorce {} occurs after death {} for {}"
                      .format(divorce, death, self.tool.combine_id_name(row[0], row[1])))

    def less_than_150_years_old(self):
        """
        US07 - Less then 150 years old
        :rtype: None
        """
        query = "select INDI, NAME, BIRT, DEAT from indi"
        for row in self.tool.query_info(query):
            if self.tool.get_age(row[2], row[3]) >= 150:
                print("ERROR: US07: Age is greater than or equal to 150 years for {}"
                      .format(self.tool.combine_id_name(row[0], row[1])))

    def birth_before_marriage_of_parents(self):
        """
        US08 - Birth before marriage of parents
        :rtype: None
        """
        query = "select indi.INDI, indi.NAME, indi.BIRT, fam.MARR, fam.DIV from indi left join fam on indi.FAMC = " \
                "fam.FAM "
        for row in self.tool.query_info(query):
            birth = row[2]
            marry = row[3]
            divorce = row[4]
            if not self.tool.date_before(marry, birth):
                print("ERROR: US08: Parent marriage {} after birth {} of {}"
                      .format(marry, birth, self.tool.combine_id_name(row[0], row[1])))
            if self.tool.date_before(divorce, birth) and not self.tool.dates_within(divorce, birth, 9, "months"):
                print("ERROR: US08: {} was born {} after 9 months of parent divorce {}".format(self.tool.combine_id_name(row[0], row[1]), birth, divorce))

    def run_sprint1(self):
        self.tool.print_info()
        self.dates_before_current_date()
        self.birth_before_marriage()
        self.birth_before_death()
        self.marriage_before_divorce()
        self.marriage_before_death()
        self.divorce_before_death()
        self.less_than_150_years_old()
        self.birth_before_marriage_of_parents()
        self.tool.disconnect()


def main():
    demo = Sprint1()
    demo.run_sprint1()


if __name__ == '__main__':
    main()

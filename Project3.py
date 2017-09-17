import sqlite3
import datetime
from prettytable import PrettyTable


class OpenSavePrint:
    def open_file(self):
        while True:
            file_name = input('Enter the file name: ')  # MyFamily.ged
            try:
                opened_file = open(file_name)  # use with is better
                break
            except (FileNotFoundError, OSError):
                print('File', file_name, 'cannot be opened. Please enter again.')
                continue
        return opened_file

    def create_table(self):
        conn = sqlite3.connect('project.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS indi(NAME TEXT, SEX TEXT, BIRT TEXT, DEAT TEXT, FAMC TEXT, FAMS TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS indi_fam(INDI TEXT, FAM TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS fam(MARR TEXT, HUSB TEXT, WIFE TEXT, CHIL TEXT, DIV TEXT)")
        c.close()
        conn.close()
    def parse_lines(self):
        conn = sqlite3.connect('project.db')
        c = conn.cursor()

        indi_non_date_keys = ["NAME", "SEX", "FAMC", "FAMS"]  # 1
        indi_date_keys = ["BIRT", "DEAT"]  # 1
        fam_non_date_keys = ["HUSB", "WIFE", "CHIL"]  # 1
        fam_date_keys = ["MARR", "DIV"]  # 1
        # individuals = {}
        # {"indi_id": {"NAME": "", "SEX": "", "BIRT": "", "DEAT": "", "FAMC": "", "FAMS": ""}}
        # families = {}
        # {"fam_id": {"MARR": "", "DIV": "", "HUSB": "", "WIFE": ""}}
        lines = self.open_file()
        date_name_cache = indi_id = fam_id = ""
        NAME = SEX = FAMC = FAMS = BIRT = DEAT = ""
        MARR = HUSB = WIFE = CHIL = DIV = ""

        for line in lines:
            words = line.strip().split()
            if words[0] == "0":
                if words[-1] == "INDI":
                    if indi_id != "":
                        c.execute("INSERT INTO indi (NAME, SEX, BIRT, DEAT, FAMC, FAMS) VALUES (?, ?, ?, ?, ?, ?)",
                                  (NAME, SEX, BIRT, DEAT, FAMC, FAMS))
                        conn.commit()
                        #  add to database
                        NAME = SEX = FAMC = FAMS = BIRT = DEAT = ""
                    else:
                        indi_id = words[1]
                if words[-1] == "FAM":
                    if indi_id != "":
                        c.execute("INSERT INTO fam (MARR, HUSB, WIFE, CHIL, DIV) VALUES (?, ?, ?, ?, ?)",
                            (MARR, HUSB, WIFE, CHIL, DIV))
                        # add to database
                        MARR = HUSB = WIFE = CHIL = DIV = ""
                    else:
                        fam_id = words[1]
            elif words[0] == "1":  # other valid cases
                if words[1] in indi_non_date_keys:
                    individuals[indi_id][words[1]] = " ".join(words[2:])
                elif words[1] in fam_non_date_keys:
                    families[fam_id][words[1]] = " ".join(words[2:])
                else:
                    date_name_cache = words[1]  # cache it for "DATE"
            elif words[0] == "2" and words[0] == "DATE":  # "DATE"
                if date_name_cache in indi_date_keys:
                    individuals[indi_id][date_name_cache] = " ".join(words[2:])
                    date_name_cache = ""
                elif date_name_cache in fam_date_keys:
                    families[fam_id][date_name_cache] = " ".join(words[2:])
                    date_name_cache = ""
                else:
                    print("Something is wrong with the date_name_cache!")
            else:
                pass

            if date_name_cache != "":
        c.close()
        conn.close()
    def get_info(self):


    def print_table(self):
        individual = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        family = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])

        # TODO: Populate two tables by using data from two dictionaries
        # Take care of "age","alive", "Husband Name","Wife Name"




def main():
    test = OpenSavePrint()
    test.parse_lines()  # for testing


if __name__ == '__main__':
    main()

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
        c.execute("CREATE TABLE IF NOT EXISTS indi(INDI TEXT, NAME TEXT, SEX TEXT, BIRT TEXT, DEAT TEXT, FAMC TEXT, FAMS TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS indi_fam(INDI TEXT, FAM TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS fam(FAM TEXT, MARR TEXT, HUSB TEXT, WIFE TEXT, CHIL TEXT, DIV TEXT)")
        c.close()
        conn.close()
    def parse_lines(self):
        conn = sqlite3.connect('project.db')
        c = conn.cursor()

        # indi_non_date_keys = ["NAME", "SEX", "FAMC", "FAMS"]  # 1
        # indi_date_keys = ["BIRT", "DEAT"]  # 1
        # fam_non_date_keys = ["HUSB", "WIFE", "CHIL"]  # 1
        # fam_date_keys = ["MARR", "DIV"]  # 1
        # individuals = {}
        # {"indi_id": {"NAME": "", "SEX": "", "BIRT": "", "DEAT": "", "FAMC": "", "FAMS": ""}}
        # families = {}
        # {"fam_id": {"MARR": "", "DIV": "", "HUSB": "", "WIFE": ""}}
        date_tags = ["BIRT", "DEAT", "MARR", "DIV"]
        lines = self.open_file()
        date_name_cache = indi_id = fam_id = ""
        indi_tab = {"INDI": "", "NAME": "", "SEX": "", "FAMC": "", "FAMS": "", "BIRT": "", "DEAT": ""}
        # INDI = NAME = SEX = FAMC = FAMS = BIRT = DEAT = ""
        FAM = MARR = HUSB = WIFE = CHIL = DIV = ""

        for line in lines:
            words = line.strip().split()
            if words[0] == "0":
                if words[-1] == "INDI":
                    if indi_id != "":
                        c.execute("INSERT INTO indi (NAME, SEX, BIRT, DEAT, FAMC, FAMS) VALUES (?, ?, ?, ?, ?, ?)",
                                  (indi_tab["INDI"], indi_tab["NAME"], indi_tab["SEX"], indi_tab["FAMC"], indi_tab["FAMS"], indi_tab["BIRT"], indi_tab["DEAT"]))
                        conn.commit()
                        INDI = NAME = SEX = FAMC = FAMS = BIRT = DEAT = ""
                    else:
                        INDI = words[1]
                if words[-1] == "FAM":
                    if indi_id != "":
                        c.execute("INSERT INTO fam (MARR, HUSB, WIFE, CHIL, DIV) VALUES (?, ?, ?, ?, ?)",
                            (MARR, HUSB, WIFE, CHIL, DIV))
                        conn.commit()
                        FAM = MARR = HUSB = WIFE = CHIL = DIV = ""
                    else:
                        FAM = words[1]
            elif words[0] == "1":
                # if words[1] in indi_tab:
                #     NAME = " ".join(words[2:])
                # elif words[1] == "SEX":
                #     SEX = " ".join(words[2:])
                # elif words[1] == "FAMC":
                #     FAMC = " ".join(words[2:])
                # elif words[1] == "FAMS":
                #     FAMS = " ".join(words[2:])
                # elif words[1] == "HUSB":
                #     HUSB = " ".join(words[2:])
                # elif words[1] == "WIFE":
                #     WIFE = " ".join(words[2:])
                # elif words[1] == "CHIL":
                #     CHIL = " ".join(words[2:])
                if words[1] in date_tags:
                    date_name_cache = words[1]  # cache it for "DATE"
                elif words[1] in indi_tab:
                    indi_tab[words[1]] = " ".join(words[2:])
                elif words[1] in fam_tab:
                    fam_tab[words[1]] = " ".join(words[2:])

                else:
                    pass

                date_tags.index()
            elif words[0] == "2" and words[0] == "DATE":
                if date_name_cache == "BIRT":
                    BIRT = " ".join(words[2:])
                elif date_name_cache == "DEAT":
                    DEAT = " ".join(words[2:])
                elif date_name_cache == "MARR":
                    MARR = " ".join(words[2:])
                elif date_name_cache == "DIV":
                    DIV = " ".join(words[2:])
                else:
                    print("Something is wrong with the date_name_cache!")
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

import sqlite3
import datetime  # should be used later
from prettytable import PrettyTable


class Project3:
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

    def create_table(self, c):

        c.execute("CREATE TABLE IF NOT EXISTS indi(INDI TEXT, NAME TEXT, SEX TEXT, BIRT TEXT, DEAT TEXT, FAMC TEXT, "
                  "FAMS TEXT)")
        # c.execute("CREATE TABLE IF NOT EXISTS indi_fam(INDI TEXT, FAM TEXT)")  # will be used in future projects
        c.execute(
            "CREATE TABLE IF NOT EXISTS fam(FAM TEXT, MARR TEXT, DIV TEXT, HUSB TEXT, WIFE TEXT, CHIL TEXT)")  # CHIL's type may be wrong
        # commit?

    def parse_lines(self, c, conn):

        indi_tab = {"INDI": "NA", "NAME": "NA", "SEX": "NA", "BIRT": "NA", "DEAT": "NA", "FAMC": "NA", "FAMS": "NA"}

        fam_tab = {"FAM": "NA", "MARR": "NA", "DIV": "NA", "HUSB": "NA", "WIFE": "NA",
                   "CHIL": "NA"}  # use list instead of []
        date_tags = ["BIRT", "DEAT", "MARR", "DIV"]
        date_name_cache = ""

        lines = self.open_file()
        for line in lines:
            words = line.strip().split()
            if words[0] == "0":
                if words[-1] in indi_tab:
                    if indi_tab[words[-1]] != "":
                        data = list(indi_tab.values())
                        print(data)
                        c.execute(
                            "INSERT INTO indi (INDI, NAME, SEX, BIRT, DEAT, FAMC, FAMS) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
                        conn.commit()

                        for key in indi_tab:
                            indi_tab[key] = "NA"
                    else:
                        indi_tab[words[-1]] = words[1]
                if words[-1] in fam_tab:
                    if fam_tab[words[-1]] != "":
                        data = list(fam_tab.values())
                        print(data)
                        if isinstance(data[5], list):
                            c.execute("INSERT INTO fam (FAM, MARR, DIV, HUSB, WIFE, CHIL) VALUES (?, ?, ?, ?, ?, ?)",
                                      (data[0], data[1], data[2], data[3], data[4], ' '.join(data[5])))
                        else:
                            c.execute("INSERT INTO fam (FAM, MARR, DIV, HUSB, WIFE, CHIL) VALUES (?, ?, ?, ?, ?, ?)",
                                      (data[0], data[1], data[2], data[3], data[4], data[5]))
                        conn.commit()

                        for key in fam_tab:
                            fam_tab[key] = "NA"
                    else:
                        fam_tab[words[-1]] = words[1]
            elif words[0] == "1":
                if words[1] in date_tags:
                    date_name_cache = words[1]
                elif words[1] in indi_tab:
                    indi_tab[words[1]] = " ".join(words[2:])
                elif words[1] in fam_tab:
                    if words[1] == "CHIL":
                        # print(type(fam_tab[words[1]]))  # test
                        # print(type(fam_tab[words[1]]))  # test
                        if not isinstance(fam_tab[words[1]], list):
                            fam_tab[words[1]] = []
                        fam_tab[words[1]].append(" ".join(words[2:]))
                    else:
                        fam_tab[words[1]] = " ".join(words[2:])
                else:
                    pass
            elif words[0] == "2" and words[0] == "DATE":
                if date_name_cache in indi_tab:
                    indi_tab[date_name_cache] = " ".join(words[2:])
                    date_name_cache = ""  # optional
                elif date_name_cache in fam_tab:
                    fam_tab[date_name_cache] = " ".join(words[2:])
                    date_name_cache = ""
                else:
                    print("Something is wrong with the date_name_cache!")

    def get_indi_info(self, c):
        c.execute('SELECT INDI, NAME, SEX, BIRT, DEAT, FAMC, FAMS FROM indi')
        return c.fetchall()

    def get_fam_info(self, c):
        c.execute('SELECT FAM, MARR, DIV, HUSB, WIFE, CHIL FROM fam')
        return c.fetchall()

    def print_table(self, c):
        # indi = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        # fam = PrettyTable(
        #     ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])
        #  "age","alive", "Husband Name","Wife Name" optional for project3?
        t_indi = PrettyTable(["ID", "Name", "Gender", "Birthday", "Death", "Child", "Spouse"])
        t_fam = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Wife ID", "Children"])
        for row in self.get_indi_info(c):
            t_indi.add_row(row)
        for row in self.get_fam_info(c):
            t_fam.add_row(row)

        print(t_indi)
        print(t_fam)


def main():
    demo = Project3()  # for testing

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    demo.create_table(c)
    demo.parse_lines(c, conn)
    demo.print_table(c)

    c.close()
    conn.close()


if __name__ == '__main__':
    main()

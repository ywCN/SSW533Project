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

        c.execute("CREATE TABLE IF NOT EXISTS indi(INDI TEXT, NAME TEXT, SEX TEXT, BIRT TEXT, DEAT TEXT, FAMC TEXT, FAMS TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS indi_fam(INDI TEXT, FAM TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS fam(FAM TEXT, MARR TEXT, DIV TEXT, HUSB TEXT, WIFE TEXT, CHIL TEXT)")  # CHIL's type may be wrong
        # commit?

    def parse_lines(self, c, conn):

        indi_tab = {"INDI": "NA", "NAME": "NA", "SEX": "NA", "BIRT": "NA", "DEAT": "NA", "FAMC": "NA", "FAMS": "NA"}
        fam_tab = {"FAM": "NA", "MARR": "NA", "DIV": "NA", "HUSB": "NA", "WIFE": "NA", "CHIL": []}
        date_tags = ["BIRT", "DEAT", "MARR", "DIV"]
        date_name_cache = ""

        lines = self.open_file()
        for line in lines:
            words = line.strip().split()
            if words[0] == "0":
                if words[-1] in indi_tab:
                    if indi_tab[words[-1]] != "":
                        data = list(fam_tab.values())
                        c.execute("INSERT INTO indi (INDI, NAME, SEX, BIRT, DEAT, FAMC, FAMS) VALUES (?, ?, ?, ?, ?, ?)",
                                  (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
                        conn.commit()

                        for key in indi_tab:
                            indi_tab[key] = "NA"
                    else:
                        indi_tab[words[-1]] = words[1]
                if words[-1] in fam_tab:
                    if fam_tab[words[-1]] != "":
                        data = list(fam_tab.values())
                        c.execute("INSERT INTO fam (FAM, MARR, DIV, HUSB, WIFE, CHIL) VALUES (?, ?, ?, ?, ?)",
                            (data[0], data[1], data[2], data[3], data[4], data[5]))
                        conn.commit()

                        for key in fam_tab:
                            if isinstance(key, list):
                                fam_tab[key][:] = []
                            else:
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
        c.execute('SELECT value, datestamp FROM stuffToPlot WHERE')
        raw = c.fetchall()
        data = []
        for row in raw:
            row_data = []
            for item in row:
                row_data.append(item)

            data.append(row_data)
        return data

    def get_fam_info(self, c):
        c.execute('SELECT value, datestamp FROM stuffToPlot WHERE')
        data = c.fetchall()
        return c.fetchall()

    def print_table(self, c):
        fam_data = self.get_indi_info(c)
        fam_data = self.get_fam_info(c)
        indi = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        fam = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])

        # TODO: Populate two tables by using data from two tables
        # Take care of "age","alive", "Husband Name","Wife Name" optional for project3?




def main():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()
    demo = Project3()  # for testing
    demo.create_table(c)
    demo.parse_lines(c)
    c.close()
    conn.close()


if __name__ == '__main__':
    main()

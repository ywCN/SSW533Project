import sqlite3
from datetime import datetime


class Project3:
    def __init__(self):
        self.conn = sqlite3.connect('project.db')
        self.c = self.conn.cursor()
        self.lines = self.open_file()

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

    def create_db(self):

        self.c.execute("CREATE TABLE IF NOT EXISTS indi(INDI TEXT, NAME TEXT, SEX TEXT, BIRT TEXT, DEAT TEXT, "
                       "FAMC TEXT, FAMS TEXT)")
        # c.execute("CREATE TABLE IF NOT EXISTS indi_fam(INDI TEXT, FAM TEXT)")  # may be used in future projects
        self.c.execute("CREATE TABLE IF NOT EXISTS fam(FAM TEXT, MARR TEXT, DIV TEXT, HUSB TEXT, WIFE TEXT, CHIL TEXT)")

    def insert_entry(self, table):
        data = list(table.values())

        if len(data) == 7:
            self.c.execute("INSERT INTO indi (INDI, NAME, SEX, BIRT, DEAT, FAMC, FAMS) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

        if len(data) == 6:
            if isinstance(data[5], list):
                self.c.execute("INSERT INTO fam (FAM, MARR, DIV, HUSB, WIFE, CHIL) VALUES (?, ?, ?, ?, ?, ?)",
                               (data[0], data[1], data[2], data[3], data[4], ' '.join(data[5])))
            else:
                self.c.execute("INSERT INTO fam (FAM, MARR, DIV, HUSB, WIFE, CHIL) VALUES (?, ?, ?, ?, ?, ?)",
                               (data[0], data[1], data[2], data[3], data[4], data[5]))
        self.conn.commit()

    def populate_db(self):

        indi_tab = {"INDI": "NA", "NAME": "NA", "SEX": "NA", "BIRT": "NA", "DEAT": "NA", "FAMC": "NA", "FAMS": "NA"}

        fam_tab = {"FAM": "NA", "MARR": "NA", "DIV": "NA", "HUSB": "NA", "WIFE": "NA", "CHIL": "NA"}
        date_tags = ["BIRT", "DEAT", "MARR", "DIV"]
        date_name_cache = ""

        for line in self.lines:
            words = line.strip().split()
            if words[0] == "0":
                if words[-1] in indi_tab:
                    if indi_tab[words[-1]] == "NA":
                        indi_tab[words[-1]] = words[1]
                        continue
                    self.insert_entry(indi_tab)
                    for key in indi_tab:
                        indi_tab[key] = "NA"

                    indi_tab[words[-1]] = words[1]

                if words[-1] in fam_tab:
                    if words[1] == "F1":
                        self.insert_entry(indi_tab)
                        fam_tab[words[-1]] = words[1]
                        continue
                    self.insert_entry(fam_tab)
                    for key in fam_tab:
                        fam_tab[key] = "NA"

                    fam_tab[words[-1]] = words[1]

                if words[1] == "TRLR":
                    self.insert_entry(fam_tab)

            elif words[0] == "1":
                if words[1] in date_tags:
                    date_name_cache = words[1]
                elif words[1] in indi_tab:
                    indi_tab[words[1]] = " ".join(words[2:])
                elif words[1] in fam_tab:
                    if words[1] == "CHIL":
                        if not isinstance(fam_tab[words[1]], list):
                            fam_tab[words[1]] = []
                        fam_tab[words[1]].append(" ".join(words[2:]))
                    else:
                        fam_tab[words[1]] = " ".join(words[2:])
                else:
                    pass

            elif words[0] == "2":
                if date_name_cache in indi_tab:
                    indi_tab[date_name_cache] = str(datetime.strptime(" ".join(words[2:]), '%d %b %Y').date())
                    date_name_cache = "NA"  # optional ?
                elif date_name_cache in fam_tab:
                    fam_tab[date_name_cache] = str(datetime.strptime(" ".join(words[2:]), '%d %b %Y').date())
                    date_name_cache = "NA"
                elif date_name_cache == "NA" or date_name_cache == "":  # == "" fixed a bug but i don't know why
                    pass
                else:
                    print("Something is wrong with the date_name_cache!")

    def disconnect(self):
        self.c.close()
        self.conn.close()


def main():
    demo = Project3()
    demo.create_db()  # MyFamily.ged
    demo.populate_db()
    demo.disconnect()
    print("Database created. If you want to create a database, please renamed the old database.")


if __name__ == '__main__':
    main()

from prettytable import PrettyTable
from collections import defaultdict


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

    def parse_lines(self):

        indi_non_date_keys = ["NAME", "SEX", "FAMC", "FAMS"]  # 1
        indi_date_keys = ["BIRT", "DEAT"]  # 1
        fam_non_date_keys = ["HUSB", "WIFE", "CHIL"]  # 1
        fam_date_keys = ["MARR", "DIV"]  # 1
        individuals = {}
        # {"indi_id": {"NAME": "", "SEX": "", "BIRT": "", "DEAT": "", "FAMC": "", "FAMS": ""}}
        families = {}
        # {"fam_id": {"MARR": "", "DIV": "", "HUSB": "", "WIFE": "", "CHIL": []}}
        lines = self.open_file()
        date_name_cache = ""
        indi_id = ""
        fam_id = ""
        for line in lines:
            words = line.strip().split()
            if words[0] == "0":  # "INDI", "FAM"
                if words[-1] == "INDI":
                    indi_id = words[1]  # [1:-1] remove @@ from source file?
                    individuals[indi_id] = {}
                if words[-1] == "FAM":
                    fam_id = words[1]  # [1:-1]
                    families[fam_id] = {}
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
                elif date_name_cache in fam_date_keys:
                    families[fam_id][date_name_cache] = " ".join(words[2:])
                else:
                    print("Something is wrong with the date_name_cache!")
            else:
                pass

        print(individuals)  # for testing
        print(families)  # for testing

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

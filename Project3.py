class OpenAndPrint:
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

    def print_lines(self):
        tags = {"0": ["HEAD", "NOTE", "INDI", "FAM", "TRLR"],
                "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                "2": ["DATE"]}

        lines = self.open_file()

        for line in lines:
            print("-->", line.strip())  # .strip() removes \r \n in the end of line

            words = line.split()
            if words[0] in tags and words[1] in tags[words[0]]:
                print("<-- " + words[0] + "|" + words[1] + "|Y|" + " ".join(words[2:]))
            elif words[0] in tags and words[-1] in tags[words[0]]:  # two special cases for INDI and FAM
                print("<-- " + words[0] + "|" + words[-1] + "|Y|" + words[1])
            else:
                print("<-- " + words[0] + "|" + words[1] + "|N|" + " ".join(words[2:]))



def main():
    test = OpenAndPrint()
    test.print_lines()


if __name__ == '__main__':
    main()

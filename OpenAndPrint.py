class OpenAndPrint:

    def open_file(self):
        while True:
            file_name = input('Enter the file name: ')
            try:
                opened_file = open(file_name)  # use with?
                break
            except FileNotFoundError:
                print('File', file_name, 'cannot be opened. Please enter again.')
                continue
        return opened_file

    def print_lines(self):
        match = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC",
                 "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL",
                 "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
        opened = self.open_file()

        for line in opened:
            print("-->", line)

            words = line.split(" ")
            len = words.__sizeof__()
            if words[1] in match:
                print(words[0], "|", words[1], "|Y|", words[2])
            elif words[-1] in match:
                print(words[0], "|", words[-1], "|Y|", words[1])
            else:
                print(words[0], "|", words[1], "|N|", words[2])



def main():
    test = OpenAndPrint()
    test.print_lines()


if __name__ == '__main__':
    main()
class OpenAndPrint:

    def open_file(self):
        while True:
            file_name = input('Enter the file name: ')
            try:
                opened_file = open(file_name)
                break
            except: # add exception name later
                print('File', file_name, 'cannot be opened. Please enter again.')
                continue
        return opened_file

    def print_lines(self):
        opened = self.open_file()

        for line in opened:

            print("-->", line)


def main():
    test = OpenAndPrint()
    test.print_lines()


if __name__ == '__main__':
    main()
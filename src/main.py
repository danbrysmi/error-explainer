# Python Checker by Dan Bryan-Smith

class Converter():
    """
    Turns a text file containing Python into a series of objects.
    """

    def __init__(self, file):
        self.block_starters = ["if", "elif", "else", "while", "for"]
        f = open(f"data/{file}", "r")
        self.lines = f.readlines()

        print("Initial")
        # removing "\n" from end of each line in text file
        self.lines[:-1] = list(map(lambda x: x[:-1], self.lines[:-1]))
        for line in self.lines:
            print([line])

        print("Comments Removed...")
        self.lines = list(map(lambda x: self.remove_comments(x), self.lines))
        for line in self.lines:
            print([line])

        print("Checking Syntax...")
        self.lines = list(map(lambda x: self.check_syntax(x), self.lines))
        for line in self.lines:
            print([line])

        print("Newlines and Deleted Lines Removed...")
        self.lines = list(filter(lambda x: self.filter_newlines(x), self.lines))
        for line in self.lines:
            print([line])


    # TIDYING UP THE CODE
    def filter_newlines(self, line): # Can be called on a line
        return line != "\n" and line != ""

    def remove_comments(self, line): #replaces with uncommented line, or just \n if whole line is deleted
        if "#" not in list(line):
            return line

        if self.char_in_quotes(line.find("#"), line):
            return line
        else:
            return line[:line.find("#")]

        return line.strip()[0] != "#"

    # UTIL?
    def char_in_quotes(self, char_index, line):
        char_list = list(line)
        q1_count = 0
        #q2_count = 0
        for i in range(char_index+1):
            #if char_list[i] == "'":
                #q1_count += 1
            if char_list[i] == '"':
                q1_count += 1
        return (q1_count % 2) != 0

    def missing_colon(self, line):
        l = line.strip()
        if len(l.split()) == 0:
            return line
        if l.split()[0] in self.block_starters:
            if l[-1] != ":":
                return line + "<:>"
            else:
                return line
        else:
            return line

    def check_syntax(self, line):
        line1 = self.missing_colon(line)
        return line1

converter = Converter("python.txt")

""" CONVERSION RULES
# Expr = Comment
" Expr = Quote Expr
Name () = Function
f " = FString
"""

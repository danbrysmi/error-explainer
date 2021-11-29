# Python Checker by Dan Bryan-Smith

class Converter():
    """
    Turns a text file containing Python into a series of objects.
    """

    def __init__(self, file):
        f = open(f"data/{file}", "r")
        self.lines = f.readlines()
        print("Initial")
        for line in self.lines:
            print([line])

        self.lines = list(map(lambda x: self.remove_comments(x), self.lines))
        print("Comments Removed...")
        for line in self.lines:
            print([line])

        self.lines = list(filter(lambda x: self.filter_newlines(x), self.lines))
        print("Newlines and Deleted Lines Removed...")
        for line in self.lines:
            print([line])




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

converter = Converter("python.txt")

""" CONVERSION RULES
# Expr = Comment
" Expr = Quote Expr
Name () = Function
f " = FString
"""

## testcase
# this is a test
print("Eggs")
## typeerror
print(1 + "A")
#>>> TypeError: unsupported operand type(s) for +: 'int' and 'str'

print("1" + "A")
#>>> "1A"
## attributeerror
message = "Hello"
message.append(" World!")
#>>> AttributeError: 'str' object has no attribute 'append'

message = "Hello"
message += " World!"
print(message)
#>>> "Hello World!"
## stringoutofrange
name = "Jester"
for i in range(7):
    print(name[i], end="")
#>>> IndexError: string index out of range

name = "Jester"
for i in range(6):
    print(name[i], end="")
    #>>> Jester
## listoutofrange
names = ["Jester", "Fjord", "Yasha"]
for i in range(4):
    print(names[i], end=" ")
#>>> IndexError: string index out of range

names = ["Jester", "Fjord", "Yasha"]
for i in range(3):
    print(names[i], end=" ")
    #>>> Jester Fjord Yasha
## END

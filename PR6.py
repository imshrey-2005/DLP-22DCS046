position = 0

def parse(input_string):
    global position
    position = 0

    if S(input_string) and position == len(input_string):
        return "Valid string"
    return "Invalid string"

def S(input_string):
    global position
    if position < len(input_string) and input_string[position] == '(':
        position += 1
        if L(input_string):
            if position < len(input_string) and input_string[position] == ')':
                position += 1
                return True
    elif position < len(input_string) and input_string[position] == 'a':
        position += 1
        return True
    return False

def L(input_string):
    global position
    if S(input_string):
        return L_prime(input_string)
    return False

def L_prime(input_string):
    global position
    if position < len(input_string) and input_string[position] == ',':
        position += 1
        if S(input_string):
            return L_prime(input_string)
    return True

def validate_string(input_string):
    return parse(input_string)

while True:
    print(validate_string(input("Enter String: ")))
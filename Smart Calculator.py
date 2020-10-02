var_dict = {}


# ('(', '^', '+', '-', '*', '/')
# Stacks the list into a postfix expression
def to_stack(lst):
    fin_stack = []
    temp_stack = []  # Stack for temporary operations

    for i in range(-len(lst), 0):
        i2 = lst[i + 1]

        if lst[i].isnumeric() or lst[i].isalpha():
            try:
                fin_stack.append(int(lst[i]))
            except ValueError:
                try:
                    fin_stack.append(var_dict[lst[i]])
                except KeyError:
                    print('Unknown variable')

            if i2 != '(' and len(fin_stack) > 1:
                if temp_stack[-1] == '^':
                    fin_stack.append(temp_stack.pop())
                elif temp_stack[-1] in ('*', '/') and i2 != '^':
                    fin_stack.append(temp_stack.pop())
                elif temp_stack[-1] in ('+', '-') and i2 not in ('^', '*', '/'):
                    fin_stack.append(temp_stack.pop())
        elif lst[i] == ")":
            last = temp_stack.pop()
            while last != "(":
                fin_stack.append(last)
                last = temp_stack.pop()
            if temp_stack[-1] in ('*', '/') and i2 != '^':
                fin_stack.append(temp_stack.pop())
        else:
            temp_stack.append(lst[i])
    for _ in range(len(temp_stack)):
        fin_stack.append(temp_stack.pop())
    return fin_stack


# Solve the postfix expression stack
def solve(stack):
    temp_stack = []
    for x in stack:
        temp_stack.append(x)
        if temp_stack[-1] in ("+", "-", "*", "/", "^"):

            temp_stack.append(operations(temp_stack.pop(), temp_stack.pop(), temp_stack.pop()))

    return temp_stack[0]


# Solves the basic operations
def operations(op, b, a):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    elif op == "^":
        return a ** b


# Turns the inputted expression into a list for easier manipulation and checks for duplicate operations outside of scope
# and clears redundant + and - in the operations
def clean(exp):
    exp_lst = [exp[0]]
    for x in range(1, len(exp)):
        if exp[x].isnumeric():
            if exp_lst[-1].isnumeric():
                exp_lst.append(exp_lst.pop() + exp[x])
            else:
                exp_lst.append(exp[x])
        elif exp[x] != " ":
            if exp[x] == '+' and exp_lst[-1] == exp[x]:
                pass
            elif exp[x] == '-' and exp_lst[-1] in ('+', '-'):
                sub = exp_lst.pop()
                if sub == '-':
                    exp_lst.append('+')
                elif sub == '+':
                    exp_lst.append('-')
            elif exp[x] == exp_lst[-1] == '^' or exp[x] == exp_lst[-1] == '*' or exp[x] == exp_lst[-1] == '/':
                return 1
            else:
                exp_lst.append(exp[x])
            '''
            elif exp[x] == '*' and (exp_lst[-1] == '*' or exp_lst[-1] == '**'):
                if exp_lst[-1] == '*':
                    exp_lst.append(exp_lst.pop() + exp[x])
                elif exp_lst[-1] == '**':
                    return 1
            elif exp[x] == '/' and (exp_lst[-1] == '/' or exp_lst[-1] == '//'):
                if exp_lst[-1] == '/':
                    exp_lst.append(exp_lst.pop() + exp[x])
                elif exp_lst[-1] == '//':
                    return 1
            '''
    return exp_lst


# Checks the expression for '/' and the validity for assignment or solving
def check(exp):
    if '/exit' == exp:
        print('Bye')
        exit()
    elif '/help' == exp:
        print('''The program calculates the sum and difference of numbers of numbers, 
        as well as ensuring the right operations are used. It also handles exceptions.
        It can store variables too''')
    elif '/' == exp[0]:
        print('Unknown command')
    elif exp[-1] in ('+', '-', '*', '/', '^') or exp[0] in ('*', '/', '^') or (exp.count('(') != exp.count(')')):
        print("Invalid expression")
    elif exp.count('=') > 1:
        print('Invalid assignment')
    elif exp.isalpha() and exp not in var_dict:
        print('Unknown variable')
    else:
        return True


# Assigns the value to the variable
def assign(exp):
    variable, value = exp.split('=')
    variable = variable.strip()
    value = value.strip()

    if not variable.isalpha() or not (value.isalpha() or value.isnumeric()):
        print('Invalid Identifier')
    elif value.isalpha():
        try:
            var_dict[variable] = var_dict[value]
        except KeyError:
            print('Unknown variable')
    else:
        var_dict[variable] = int(value)


# Main Code
while True:
    expression = input().strip()

    if expression.startswith("+"):
        expression = expression[1:]
    elif len(expression) == 0:
        pass
    elif check(expression):
        if '=' in expression:
            assign(expression)
        else:
            expression = clean(expression)
            if expression == 1:
                print('Invalid Expression')
            else:
                print(int(solve(to_stack(expression))))

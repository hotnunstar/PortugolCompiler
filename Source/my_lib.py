# my_lib.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

from logic_grammar import LogicGrammar


def run_batch(filename, op):
    with open(filename, "r", encoding="utf8") as f:
        content = f.read()
        lg = LogicGrammar()
        try:
            if op == "1":
                ans = lg.parse(content)
            if op == "2":
                ans = lg.parse_c(content)
            if ans is not None:
                print(ans)
        except Exception as exception:
            print(exception)


def v_vars(lst):
    key = []
    value = []
    if type(lst) is dict:
        for a, b in lst.items():
            key.append(a)
            value.append(b)
    elif type(lst) is tuple:
        for var in lst:
            for a, b in var.items():
                key.append(a)
                value.append(b)
    elif type(lst) is list:
        for var in lst:
            for a, b in var.items():
                key.append(a)
                value.append(b)
    else:
        value.append(str(lst))
    return value


def v_vars_c(lst):
    if type(lst) is dict:
        for a, b in lst.items():
            a = v_type(a)
            b = a + " " + b
    elif type(lst) is tuple:
        for var in lst:
            for a, b in var.items():
                a = v_type(a)
                b = a + " " + b
    elif type(lst) is list:
        for var in lst:
            for a, b in var.items():
                a = v_type(a)
                b = a + " " + b
    return b


def v_type(string):
    if string == "inteiro":
        return "int"
    elif string == "real":
        return "float"
    elif string == "carater":
        return "char"
    elif string == "logico":
        return "bool"
    elif string == "void":
        return "void"
    else:
        print(f"Unknown type of variable {string}")

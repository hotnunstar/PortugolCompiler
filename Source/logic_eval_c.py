# logic_eval.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

import my_lib


class LogicEvalC:
    list_int = []
    list_float = []
    list_char = []
    list_bool = []

    # Dispatch Table (Design Pattern)
    operators = {
        "ou": lambda args: str(args[0]) + " || " + str(args[1]),
        "e": lambda args: str(args[0]) + " && " + str(args[1]),
        "xou": lambda a: str(a[0]) + " ^ " + str(a[1]),
        "nao": lambda a: " ! " + str(a[0]),
        "+": lambda args: str(args[0]) + " + " + str(args[1]),
        "-": lambda args: str(args[0]) + " - " + str(args[1]),
        "*": lambda args: str(args[0]) + " * " + str(args[1]),
        "/": lambda args: str(args[0]) + " / " + str(args[1]),
        "<": lambda args: str(args[0]) + " < " + str(args[1]),
        ">": lambda args: str(args[0]) + " > " + str(args[1]),
        "!=": lambda args: str(args[0]) + " != " + str(args[1]),
        "==": lambda args: str(args[0]) + " == " + str(args[1]),
        ">=": lambda args: str(args[0]) + " >= " + str(args[1]),
        "<=": lambda args: str(args[0]) + " <= " + str(args[1]),

        "assign": lambda a: LogicEvalC._assign(*a),
        "escreva": lambda a: LogicEvalC._output(a),
        "leia": lambda a: LogicEvalC._input(a),
        "if": lambda args: LogicEvalC._if(*args),
        "if_else": lambda args: LogicEvalC._if_else(*args),
        "while": lambda args: LogicEvalC._while(*args),
        "for": lambda args: LogicEvalC._for(*args),
        "fun": lambda args: LogicEvalC._fun(args),
        "call": lambda args: LogicEvalC._call(args),
    }

    @staticmethod
    def _assign(var, value):
        print("\t"+var+" = "+str(value)+";")

    @staticmethod
    def _output(values):    # Não está a adicionar o "%s" referente ao tipo de dados impresso
        var = ""
        for value in values:
            var += value + ", "
        var = var[:-2]
        print("\tprintf("+var+");")

    @staticmethod
    def _input(values):     # faz a identificação do tipo de dados da variável
        s = ""
        var = ""
        for val in values:
            if val in LogicEvalC.list_int:
                s += "%d "
            elif val in LogicEvalC.list_float:
                s += "%f "
            else:
                s += "%s "
            var += "&" + val + ", "
        s = s[:-1]
        var = var[:-2]
        print("\n\tscanf(\""+s+"\", "+var+");")

    @staticmethod
    def _if(cond, code):
        print("COND:", cond)
        print("\n\tif ("+cond+")\n\t{")
        LogicEvalC.eval(code)
        print("\t}")

    @staticmethod
    def _if_else(cond, code1, code2):
        print("\n\tif (" + cond + ")\n\t{")
        LogicEvalC.eval(code1)
        print("\t}")
        print("\telse\n\t{")
        LogicEvalC.eval(code2)
        print("\t}")

    @staticmethod
    def _while(cond, code):
        print("\n\twhile ("+cond+")\n\t{")
        LogicEvalC.eval(code)
        print("\t}")

    @staticmethod
    def _for(var, lower, higher, inc, code):
        print("\n\tfor ("+var+"="+str(lower)+"; "+var+"="+str(higher)+"; "+var+"="+var+"+"+str(inc)+")\n\t{")
        LogicEvalC.eval(code)
        print("\t}")

    @staticmethod
    def _fun(args):
        var_type, name, var, code = args
        vars = ""
        if len(var) == 1:
            vars = var[var_type]
        else:
            for v in var:
                vars += my_lib.v_vars_c(v) + ", "
            vars = vars[:-2]
        var_type = my_lib.v_type(var_type)
        signature = var_type + " " + name + "("+vars+");"
        print(signature)

    @staticmethod
    def _call(args):
        name, values = args
        vars = []
        vals = ""
        for v in values:
            vars += my_lib.v_vars(v)
        for v in vars:
            vals += v + ", "
        vals = vals[:-2]
        text = name+"("+vals+")"
        return text

    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(LogicEvalC.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]
            if op in LogicEvalC.operators:
                func = LogicEvalC.operators[op]
                return func(args)
        elif "funct" in ast:
            funct = ast["funct"]
            args = list(map(LogicEvalC.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]
            if funct in LogicEvalC.operators:
                func = LogicEvalC.operators[funct]
                return func(args)
        elif "inteiro" in ast:
            values = "int "
            for var in ast["inteiro"]:
                LogicEvalC.list_int.append(var)
                values += var + ", "
            values = values[:-2]
            print("\t" + values + ";")
        elif "real" in ast:
            values = "float "
            for var in ast["real"]:
                LogicEvalC.list_float.append(var)
                values += var + ", "
            values = values[:-2]
            print("\t" + values + ";")
        elif "carater" in ast:
            values = "char "
            for var in ast["carater"]:
                LogicEvalC.list_char.append(var)
                values += var + ", "
            values = values[:-2]
            print("\t" + values + ";")
        elif "logico" in ast:
            values = "bool "
            for var in ast["logico"]:
                LogicEvalC.list_bool.append(var)
                values += var + ", "
            values = values[:-2]
            print("\t" + values + ";")
        elif "varName" in ast:
            for var in ast["varName"]:
                return var
        else:
            raise Exception("Weird dict on eval")

    @staticmethod
    def eval(ast):
        if type(ast) in (int, float, bool, str):
            return ast
        if type(ast) is dict:
            return LogicEvalC._eval_dict(ast)
        if type(ast) is list:
            for c in ast:
                ans = LogicEvalC._eval_dict(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")



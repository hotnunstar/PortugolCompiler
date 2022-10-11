# logic_eval.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

from symbol_table import SymbolTable
import my_lib


class LogicEval:
    list_int = []
    list_float = []
    list_char = []
    list_bool = []

    # Dispatch Table (Design Pattern)
    operators = {
        "ou": lambda args: args[0] or args[1],
        "e": lambda args: args[0] and args[1],
        "xou": lambda a: a[0] ^ a[1],
        "nao": lambda a: not a[0],
        "+": lambda args: args[0] + args[1],
        "-": lambda args: args[0] - args[1],
        "*": lambda args: args[0] * args[1],
        "/": lambda args: args[0] / args[1],
        "<": lambda args: args[0] < args[1],
        ">": lambda args: args[0] > args[1],
        "!=": lambda args: args[0] != args[1],
        "==": lambda args: args[0] == args[1],
        ">=": lambda args: args[0] >= args[1],
        "<=": lambda args: args[0] <= args[1],

        "assign": lambda a: LogicEval._assign(*a),
        "escreva": lambda a: print(*a),
        "leia": lambda a: LogicEval._input(a),
        "if": lambda args: LogicEval._if(*args),
        "if_else": lambda args: LogicEval._if_else(*args),
        "while": lambda args: LogicEval._while(*args),
        "for": lambda args: LogicEval._for(*args),
        "fun": lambda args: LogicEval._fun(args),
        "call": lambda args: LogicEval._call(args),
    }

    symbols = SymbolTable()     # Symbol Table (Tabela de Símbolos)

    @staticmethod
    def _assign(var, value):
        if var in LogicEval.list_int:
            try:
                LogicEval.symbols[var] = int(value)
            except Exception:
                print(f"{value} isn't integer")
        elif var in LogicEval.list_float:
            try:
                LogicEval.symbols[var] = float(value)
            except Exception:
                print(f"{value} isn't float")
        elif var in LogicEval.list_char:
            try:
                LogicEval.symbols[var] = str(value)
            except Exception:
                print(f"{value} isn't char")
        elif var in LogicEval.list_bool:
            try:
                LogicEval.symbols[var] = bool(value)
            except Exception:
                print(f"{value} isn't bool")
        else:
            LogicEval.symbols[var] = value

    @staticmethod
    def _input(values):
        for value in values:
            aux = input("<-")
            LogicEval._assign(value["varName"], aux)

    @staticmethod
    def _if(cond, code):
        if cond:
            LogicEval.eval(code)

    @staticmethod
    def _if_else(cond, code1, code2):
        if cond:
            LogicEval.eval(code1)
        else:
            LogicEval.eval(code2)

    @staticmethod
    def _while(value, code):
        while LogicEval.eval(value):
            LogicEval.eval(code)

    @staticmethod
    def _for(var, lower, higher, inc, code):
        comp = (lambda a, b: a != b)
        value = lower
        LogicEval._assign(var, value)
        while comp(value, higher):
            LogicEval.eval(code)
            value += inc
            LogicEval._assign(var, value)

    @staticmethod
    def _fun(args):
        var_type, name, var, code = args
        var = my_lib.v_vars(var)
        LogicEval.symbols[name] = {"vars": var, "code": code}

    @staticmethod
    def _call(args):
        name, values = args
        if name in LogicEval.symbols:
            code = LogicEval.symbols[name]["code"]
            var_list = LogicEval.symbols[name]["vars"]
            for var_name, value in zip(var_list, values):   # Definir as variaveis recebidas
                LogicEval.symbols.re_set(var_name, LogicEval.eval(value))
            result = LogicEval.eval(code)   # Avaliar Codigo
            for var in var_list:    # Apagar as variaveis "locais"
                del LogicEval.symbols[var]
            return result
        else:
            raise Exception(f"Function {name} not defined")

    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(LogicEval.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]
            if op in LogicEval.operators:
                func = LogicEval.operators[op]
                return func(args)
            else:
                raise Exception(f"Unknown operator: {op}")
        elif "funct" in ast:
            funct = ast["funct"]
            args = ast["args"]
            if "data" in ast:
                args = [args]
                args += ast["data"]
            if funct in LogicEval.operators:
                func = LogicEval.operators[funct]
                return func(args)
            else:
                raise Exception(f"Unknown operator: {funct}")
        elif "inteiro" in ast:
            for var in ast["inteiro"]:
                LogicEval.symbols[var] = None
                LogicEval.list_int.append(var)
        elif "real" in ast:
            for var in ast["real"]:
                LogicEval.symbols[var] = None
                LogicEval.list_float.append(var)
        elif "carater" in ast:
            for var in ast["carater"]:
                LogicEval.symbols[var] = None
                LogicEval.list_char.append(var)
        elif "logico" in ast:
            for var in ast["logico"]:
                LogicEval.symbols[var] = None
                LogicEval.list_bool.append(var)
        elif "varName" in ast:
            if ast["varName"] in LogicEval.symbols:
                return LogicEval.symbols[ast["varName"]]
            raise Exception(f"Unknown variable {ast['varName']}")
        else:
            raise Exception("Weird dict on eval")

    @staticmethod
    def eval(ast):
        if type(ast) in (int, float, bool, str):
            return ast
        if type(ast) is dict:
            return LogicEval._eval_dict(ast)
        if type(ast) is list:
            ans = None
            for c in ast:
                ans = LogicEval._eval_dict(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")
